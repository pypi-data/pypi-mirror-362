import logging
import re
import threading
import queue
import sys
from typing import Dict, Any, Optional, List

import fsspec
import pyarrow as pa
import pyarrow.parquet as pq

from ray.data._internal.checkpoint.checkpoint_config import CheckpointStorageConfig

fsspec.register_implementation("tos", "tosfs.TosFileSystem")

logger = logging.getLogger(__name__)


class CheckpointStorageFileSystemActor:
    """
    This actor is responsible for writing, reading, and managing checkpoints
    on a filesystem for a specific bucket.

    It is a singleton actor that is created per bucket.
    """

    def __init__(self, bucket_id: int, storage_config: CheckpointStorageConfig):
        self._bucket_id = bucket_id
        self._storage_config = storage_config

        # Get checkpoint root path from config
        options = self._storage_config.options.copy()
        path = options.pop("path", None)
        if not path:
            raise ValueError(
                "The 'path' must be specified in 'storage_config.options' (e.g., 'file:///tmp/checkpoints' or 'tos://bucket/checkpoints').")

        self._max_items_per_file = options.pop("max_items_per_file", 100000)

        # Automatically create filesystem based on path
        try:
            # fsspec will select the filesystem based on the protocol in the path (e.g., "file://", "tos://")
            try:
                fsspec_fs, fsspec_path = fsspec.core.url_to_fs(path, **options)
            except Exception as e:
                logger.error(
                    f"Failed to create filesystem for path '{path}': {e}")
                raise

            # Wrap the fsspec filesystem to be a pyarrow filesystem
            self._fs = pa.fs.PyFileSystem(pa.fs.FSSpecHandler(fsspec_fs))
        except Exception as e:
            logger.error(
                f"Failed to create filesystem for path '{fsspec_path}': {e}")
            raise
        from pathlib import Path
        # Checkpoint directory path
        self._checkpoint_dir = fsspec_path
        self._fs.create_dir(self._checkpoint_dir, recursive=True)
        self._checkpoint_prefix = str(
            Path(self._checkpoint_dir)/f"cp_bucket{self._bucket_id}_")

        self._processed_items: Optional[pa.Table] = None
        self._last_file_index: int = -1
        self._load_checkpoint()

        self._write_queue = queue.Queue()
        # A dedicated thread to write checkpoints to the filesystem.
        self._writer_thread = threading.Thread(target=self._write_loop, daemon=True)
        self._writer_thread.start()


    def _load_checkpoint(self):
        """Loads all checkpoint files from the filesystem on initialization."""
        logger.info(f"Loading checkpoint from {self._checkpoint_dir}")
        try:
            file_selector = pa.fs.FileSelector(
                self._checkpoint_dir, recursive=False)
            files = self._fs.get_file_info(file_selector)
        except FileNotFoundError:
            logger.info(
                f"Checkpoint directory {self._checkpoint_dir} does not exist, starting anew.")
            files = []
        except Exception as e:
            logger.error(f"Failed to list checkpoint files: {e}")
            raise

        all_items_tables: List[pa.Table] = []
        max_index = -1

        # Compile a regex to match checkpoint files.
        # Filename format: cp_bucket{self._bucket_id}_{index}.parquet
        filename_pattern = re.compile(
            f"cp_bucket{self._bucket_id}_(\d+)\\.parquet$")

        for file_info in files:
            if not file_info.is_file:
                continue

            match = filename_pattern.search(file_info.base_name)
            if not match:
                continue

            try:
                file_index = int(match.group(1))
                max_index = max(max_index, file_index)

                table = pq.read_table(file_info.path, filesystem=self._fs)
                if table.num_rows > 0:
                    all_items_tables.append(table)
            except Exception as e:
                logger.warning(
                    f"Failed to read or parse checkpoint file {file_info.path}: {e}")
                # Continue with other files instead of failing the entire load process.
                continue

        if all_items_tables:
            self._processed_items = pa.concat_tables(all_items_tables)
        self._last_file_index = max_index

        if self._processed_items is not None:
            logger.info(
                f"Loaded {self._processed_items.num_rows} items from {len(files)} files. The latest file index is {self._last_file_index}.")
        else:
            logger.info("No existing checkpoint found. Starting over.")

    def _write_loop(self):
        """The writer thread loop that saves batches of items to checkpoint files."""
        writer: Optional[pq.ParquetWriter] = None
        items_in_current_file = 0
        current_file_index = self._last_file_index
        checkpoint_path = ""

        try:
            while True:
                table = self._write_queue.get()
                if table is None:
                    # Sentinel value received, exit the loop.
                    logger.info("Writer thread received sentinel, shutting down.")
                    break

                try:
                    # If we need to start a new file. This is true if:
                    # 1. The writer is not initialized (first block).
                    # 2. The current file has items and adding the new block
                    #    would exceed the per-file limit.
                    if writer is None or (
                        items_in_current_file > 0
                        and items_in_current_file + table.num_rows
                        > self._max_items_per_file
                    ):
                        if writer:
                            logger.info(
                                f"Closing file {checkpoint_path} with {items_in_current_file} items."
                            )
                            writer.close()

                        current_file_index += 1
                        checkpoint_path = (
                            f"{self._checkpoint_prefix}{current_file_index}.parquet"
                        )
                        logger.info(f"Creating new checkpoint file {checkpoint_path}")
                        writer = pq.ParquetWriter(
                            checkpoint_path, table.schema, filesystem=self._fs
                        )
                        items_in_current_file = 0
                    writer.write_table(table)
                    items_in_current_file += table.num_rows
                    self._last_file_index = current_file_index
                except Exception as e:
                    logger.error(f"Failed to save checkpoint to {checkpoint_path}: {e}")
                finally:
                    self._write_queue.task_done()
        finally:
            if writer:
                writer.close()
            logger.info("Writer thread shut down.")

    def record_processed_item(
        self, table: "pa.Table", metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Records a processed block, adding its items to the processed set and
        queuing the block for writing to storage.
        This method filters out items that have already been processed.
        """
        if table.num_rows == 0:
            return

        table_to_write = table
        if self._processed_items is not None:
            # Filter out items that have already been processed.
            existing_item_ids = self._processed_items.column(0)
            new_item_ids = table.column(0)
            is_processed_mask = pa.compute.is_in(
                new_item_ids, value_set=existing_item_ids
            )
            is_not_processed_mask = pa.compute.invert(is_processed_mask)
            table_to_write = table.filter(is_not_processed_mask)

        if table_to_write.num_rows == 0:
            return

        self._write_queue.put(table_to_write)

    def get_all_processed_items(self) -> Optional["pa.Table"]:
        """Retrieves all unique processed item identifiers from the storage as a single Block."""
        return self._processed_items

    def is_item_processed(self, table: "pa.Table") -> "pa.BooleanArray":
        """Checks if a specific item has been processed."""
        if self._processed_items is None:
            # No items have been processed yet, so all are new.
            return pa.array([False] * table.num_rows, type=pa.bool_())

        existing_item_ids = self._processed_items.column(0)
        item_ids_to_check = table.column(0)

        # is_in returns a boolean array.
        is_processed_mask = pa.compute.is_in(
            item_ids_to_check, value_set=existing_item_ids
        )

        return is_processed_mask

    def on_exit(self):
        """Ensures all pending items are persisted before exiting."""
        logger.info("Persisting final checkpoint state on exit.")
        # Wait for the writer to process all items currently in the queue.
        self._write_queue.join()

        # Send sentinel to stop the writer thread and wait for it to terminate.
        self._write_queue.put(None)
        self._writer_thread.join()
        logger.info("Final checkpoint state persisted. Writer thread shut down.")
        sys.exit(0)
