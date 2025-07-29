from typing import Dict, Any, Optional, Iterable

from ray.data.block import Block, BlockAccessor
from ray.data.datasource.datasink import Datasink
from ray.data._internal.execution.interfaces import TaskContext

try:
    from confluent_kafka import Producer
except ImportError:
    raise ImportError("`confluent_kafka` not installed. Try `pip install confluent_kafka`.")


class KafkaDatasink(Datasink[None]):
    """A DataSink that writes data to a Kafka topic.

    This is a distributed sink, where each block is written to Kafka in a separate
    Ray task.
    """

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        *,
        key_column: Optional[str] = None,
        value_column: str = "value",
        producer_config: Optional[Dict[str, Any]] = None,
    ):
        """Creates a Kafka DataSink.

        Args:
            bootstrap_servers: A comma-separated list of Kafka broker addresses,
                e.g., "host1:9092,host2:9092".
            topic: The Kafka topic to write to.
            key_column: The name of the column to be used as message key. If None,
                messages will be sent without a key.
            value_column: The name of the column to be used as message value.
                Defaults to "value".
            producer_config: A dictionary of Kafka producer configurations.
                An important configuration is 'acks', which controls the durability
                guarantees. To configure the flush timeout, you can pass
                `{"flush.timeout": <seconds>}`.
        """
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._key_column = key_column
        self._value_column = value_column
        self._producer_config = (producer_config or {}).copy()
        self._producer_config["bootstrap.servers"] = self._bootstrap_servers

        self._flush_timeout = self._producer_config.pop("flush.timeout", 120)

    def write(
        self,
        blocks: Iterable[Block],
        ctx: TaskContext,
    ) -> None:
        """
        Writes data to a Kafka topic.

        Args:
            blocks: An iterator of blocks to write.
            ctx: The DataContext.
        """
        producer = Producer(self._producer_config)
        topic = self._topic
        key_column = self._key_column
        value_column = self._value_column
        total_messages_produced = 0

        def _write_block(block: Block) -> int:
            """The actual write logic that runs for each block in a remote task."""
            import pyarrow as pa

            block_accessor = BlockAccessor.for_block(block)
            num_rows = block_accessor.num_rows()
            if num_rows == 0:
                return 0

            # Use columnar iteration for efficiency.
            values = block[value_column]
            keys = (
                block[key_column]
                if key_column
                else [None] * num_rows
            )

            messages_produced = 0
            for key, value in zip(keys, values):
                if value is None:
                    continue
                # If key or value are not bytes, encode them.
                if key is not None:
                    if isinstance(key, pa.lib.BinaryScalar):
                        key = key.as_py()
                    elif not isinstance(key, bytes):
                        key = str(key).encode("utf-8")
                # If value is not bytes, encode it.
                if isinstance(value, pa.lib.BinaryScalar):
                    value = value.as_py()
                elif not isinstance(value, bytes):
                    value = str(value).encode("utf-8")

                # produce() is asynchronous.
                producer.produce(topic, value=value, key=key)
                messages_produced += 1

            return messages_produced

        for block in blocks:
            total_messages_produced += _write_block(block)

        # producer.flush() will block until all buffered messages are
        # successfully sent. This ensures that all data in this task is
        # committed to the Kafka broker.
        remaining = producer.flush(timeout=self._flush_timeout)
        if remaining > 0:
            raise RuntimeError(
                f"{remaining} out of {total_messages_produced} messages failed to be "
                "delivered to Kafka within the timeout."
            )