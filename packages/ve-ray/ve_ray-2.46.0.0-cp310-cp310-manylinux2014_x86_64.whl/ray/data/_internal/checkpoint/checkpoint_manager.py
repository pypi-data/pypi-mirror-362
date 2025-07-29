from typing import Optional, Dict, Any, List, Tuple, TYPE_CHECKING
from dataclasses import dataclass
import logging

import hashlib

import ray
from ray.data.block import Block, BlockAccessor, BlockType
from ray.data._internal.checkpoint.checkpoint_config import CheckpointConfig
from ray.data._internal.checkpoint.checkpoint_storage import CheckpointStorageFileSystemActor

if TYPE_CHECKING:
    import pyarrow as pa

logger = logging.getLogger(__name__)


def create_checkpoint_manager(checkpoint_config: Optional[Dict[str, Any]] = None):
    manager = None
    if checkpoint_config is not None:
        config = CheckpointConfig(checkpoint_config)
        if config.enabled:
            logger.info(f"Checkpoint is enabled with path: "
                        f"{config.storage_config.path}")
            manager = CheckpointManager(config)
            manager.check_ready(timeout=config.storage_config.check_ready_timeout)
    return manager


@dataclass
class BucketLocation:
    """
    Represents the location of a checkpoint in storage.
    This includes the bucket ID and the index within that bucket.
    """
    bucket_id: int
    bucket_index: int

# --- Checkpoint Manager ---
class CheckpointManager:
    """
    Manages checkpoint operations for a specific dataset and operator.
    It acts as a higher-level interface over different checkpoint storage backends.
    """
    def __init__(self, checkpoint_config: CheckpointConfig):
        """
        Initializes the CheckpointManager.

        Args:
            checkpoint_config: The configuration for checkpoint.
        """
        self._checkpoint_config = checkpoint_config
        self._storage_actors = []
        if checkpoint_config.enabled:
            remote_args = self._checkpoint_config.storage_config.remote_args
            self._cls = ray.remote(
                **remote_args)(CheckpointStorageFileSystemActor)
            for i in range(self._checkpoint_config.num_buckets):
                self._storage_actors.append(
                    self._cls.remote(i, self._checkpoint_config.storage_config)
                )

    @property
    def is_enabled(self) -> bool:
        """Checks if checkpoint is enabled and configured for this manager."""
        return self._checkpoint_config.enabled

    def is_ready(self):
        """
        Checks if all checkpoint storage actors are ready.
        """
        ready = ray.get([actor.__ray_ready__.remote()
                        for actor in self._storage_actors])
        return all(ready)

    def check_ready(self, timeout: Optional[float] = None):
        """
        Checks if all checkpoint storage actors are ready.

        Args:
            timeout: The maximum time to wait for actors to become ready. If None,
                it will wait indefinitely.

        Raises:
            TimeoutError: If not all actors are ready within the specified timeout.
        """
        if self._checkpoint_config.enabled:
            ready = ray.get([actor.__ray_ready__.remote()
                            for actor in self._storage_actors], timeout=timeout)
            if not all(ready):
                raise TimeoutError("Checkpoint storage actors not ready.")

    def shutdown(self):
        # Call on_exit on all actors using a list comprehension for conciseness,
        # then clear the list. This fixes a bug in the original implementation
        # where modifying the list while iterating would skip actors.
        logger.info("Shutting down checkpoint manager.")
        for actor in self._storage_actors:
            actor.on_exit.remote()
            del actor
        self._storage_actors.clear()

    def _get_bucket_location(self, dataframe: "pandas.DataFrame", num_buckets: int) -> List[BucketLocation]:
        """
        Get the bucket location for each row in the dataframe.

        Args:
            dataframe: The pandas DataFrame to process.

        Returns:
            A list of BucketLocation, where each BucketLocation is a
              (bucket_id, index_in_bucket).
        """
        import pandas as pd

        if len(dataframe) == 0:
            return []

        key_column = dataframe[dataframe.columns[0]]
        dtype = key_column.dtype

        import numpy as np
        if np.issubdtype(dtype, np.integer):
            # For integer types, we can use modulo directly for efficiency.
            bucket_ids = key_column % num_buckets
        else:
            # For other types (float, string, object), use a stable hash
            # to ensure consistent bucketing.
            def stable_hash(x):
                return int(hashlib.sha1(str(x).encode("utf-8")).hexdigest(), 16)

            # Calculate bucket IDs for each key.
            bucket_ids = key_column.apply(stable_hash) % num_buckets

        bucket_counters = [0] * num_buckets
        bucket_location_list = [None] * len(dataframe)

        for i, bucket_id in enumerate(bucket_ids):
            index_in_bucket = bucket_counters[bucket_id]
            bucket_location_list[i] = BucketLocation(bucket_id, index_in_bucket)
            bucket_counters[bucket_id] += 1

        return bucket_location_list

    def _split_table_by_bucket(self, table: "pa.Table", num_buckets: int) -> Tuple[List["pa.Table"], List[BucketLocation]]:
        """
        Split the table into multiple buckets based on the hash of the first key column.

        Args:
            table: The pyarrow Table to process which only include the key columns.

        Returns:
            A tuple containing:
            - A list of pyarrow.Tables, where each table is a bucket.
            - A list of BucketLocation, where each BucketLocation is a
              (bucket_id, index_in_bucket).
        """

        # get the dataframe only include key columns
        df = table.to_pandas()

        bucket_location_list = self._get_bucket_location(df, num_buckets)

        bucket_indices = [[] for _ in range(num_buckets)]
        for i, bucket_location in enumerate(bucket_location_list):
            bucket_indices[bucket_location.bucket_id].append(i)

        buckets = []
        for indices in bucket_indices:
            if len(indices) > 0:
                buckets.append(table.take(indices))
            else:
                buckets.append(None)

        return buckets, bucket_location_list

    # follow functions were invoked in worker
    def skip_processed_row(self, block: Block) -> Block:
        if self._checkpoint_config.num_buckets == 0:
            return block
        num_buckets = self._checkpoint_config.num_buckets
        key_columns = self._checkpoint_config.key_columns
        block_accessor = BlockAccessor.for_block(block)
        if not all(x in block_accessor.column_names() for x in key_columns):
            raise ValueError(
                f"Key column '{key_columns}' not found in block.")
        if block_accessor.num_rows() == 0:
            return block
        # only To use pandas for easy hashing and grouping.
        import pyarrow as pa
        if block_accessor.block_type() == BlockType.ARROW:
            table = block_accessor.select(key_columns)
        else:
            table = pa.Table.from_pandas(block_accessor.select(key_columns))
        # split the table into multiple buckets
        buckets, bucket_location_list = self._split_table_by_bucket(
            table, num_buckets)

        futures = {}
        for bucket_index, bucket_table in enumerate(buckets):
            if bucket_table and bucket_table.num_rows > 0:
                actor = self._storage_actors[bucket_index]
                futures[bucket_index] = actor.is_item_processed.remote(
                    bucket_table)

        processed_masks_by_bucket = {
            index: ray.get(future) for index, future in futures.items()
        }

        num_rows = block_accessor.num_rows()
        is_processed_list = [False] * num_rows

        for i, location in enumerate(bucket_location_list):
            bucket_id = location.bucket_id
            index_in_bucket = location.bucket_index

            if bucket_id in processed_masks_by_bucket:
                mask_for_bucket = processed_masks_by_bucket[bucket_id]
                if mask_for_bucket[index_in_bucket].as_py():
                    is_processed_list[i] = True

        # If no rows were processed, return the original block to avoid
        # unnecessary copying.
        if not any(is_processed_list):
            return block

        import pyarrow.compute as pc

        # We want to keep rows that are NOT processed.
        keep_mask = pc.invert(pa.array(is_processed_list))

        if block_accessor.block_type() == BlockType.ARROW:
            # The block is a pyarrow.Table, which has a .filter() method.
            return block.filter(keep_mask)
        elif block_accessor.block_type() == BlockType.PANDAS:
            # The block is a pandas.DataFrame. We convert the Arrow boolean mask
            # to a numpy array for boolean indexing.
            return block[keep_mask.to_numpy()]

    def record_data_block(self, block: Block):
        """
        Extracts keys from a block, hashes them to determine the correct
        bucket, and calls the corresponding CheckpointStorageActor to record
        the processed items.

        Args:
            block: The block of data being processed.
        """
        if self._checkpoint_config.num_buckets == 0:
            return

        num_buckets = self._checkpoint_config.num_buckets
        key_columns = self._checkpoint_config.key_columns
        block_accessor = BlockAccessor.for_block(block)
        if not all(x in block_accessor.column_names() for x in key_columns):
            raise ValueError(
                f"Key column '{key_columns}' not found in block.")
        if block_accessor.num_rows() == 0:
            return
        # use pyarrow to split.
        import pyarrow as pa
        if block_accessor.block_type() == BlockType.ARROW:
            table = block_accessor.select(key_columns)
        else:
            table = pa.Table.from_pandas(block_accessor.select(key_columns))
        # split the table into multiple buckets
        buckets, _ = self._split_table_by_bucket(table, num_buckets)
        for bucket_index, bucket_table in enumerate(buckets):
            if bucket_table and bucket_table.num_rows > 0:
                actor = self._storage_actors[bucket_index]
                actor.record_processed_item.remote(bucket_table)
