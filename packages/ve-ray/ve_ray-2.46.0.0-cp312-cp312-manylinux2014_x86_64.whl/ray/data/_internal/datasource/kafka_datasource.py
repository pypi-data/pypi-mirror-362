import logging
from typing import List, Dict, Any, Optional, Iterator

import numpy as np

import ray
from ray.data.block import Block, BlockAccessor, BlockMetadata
from ray.data.datasource.datasource import Datasource, ReadTask

logger = logging.getLogger(__name__)

try:
    from confluent_kafka import Consumer, TopicPartition, KafkaException
    from confluent_kafka.cimpl import KafkaError
except ImportError:
    raise ImportError("`confluent_kafka` not installed. Try `pip install confluent_kafka`.")


def _read_kafka_task(
    topic: str,
    partitions: List[int],
    consumer_config: Dict[str, Any],
    poll_timeout: float,
    message_batch_size: int,
) -> Iterator[Block]:
    """The actual read logic that runs in a Ray Task."""
    consumer = Consumer(consumer_config)
    topic_partitions = [TopicPartition(topic, p) for p in partitions]
    consumer.assign(topic_partitions)
    total_messages = 0
    logger.info(f"Start consuming kafka partitions {partitions} ")
    try:
        while True:
            messages = consumer.consume(
                num_messages=message_batch_size, timeout=poll_timeout
            )
            if not messages:
                # If no messages, continue polling. This is a streaming source.
                continue

            # Use a columnar format to build the block, which is more efficient
            # than creating a list of dictionaries.
            output_columns = {
                "key": [],
                "value": [],
                "topic": [],
                "partition": [],
                "offset": [],
                "timestamp": [],
                "headers": [],
            }
            has_data = False
            for msg in messages:
                err = msg.error()
                if err:
                    # Reaching the end of a partition is not a real error for streaming.
                    if err.code() == KafkaError._PARTITION_EOF:
                        continue
                    raise KafkaException(err)

                has_data = True
                output_columns["key"].append(msg.key())
                output_columns["value"].append(msg.value())
                output_columns["topic"].append(msg.topic())
                output_columns["partition"].append(msg.partition())
                output_columns["offset"].append(msg.offset())
                output_columns["timestamp"].append(
                    msg.timestamp()[1])  # (type, ms)
                output_columns["headers"].append(msg.headers())

            if has_data:
                total_messages += len(output_columns['value'])
                if total_messages % 10000 == 0:
                    logger.info(
                        f"Read kafka {partitions} {total_messages} messages")
                yield BlockAccessor.batch_to_block(output_columns)
    finally:
        consumer.close()


class KafkaDatasource(Datasource):
    """A datasource that reads data from Kafka topics.

    Example:
        >>> import ray
        >>> from ray.data.datasource import KafkaDatasource
        >>> # Create a dataset from Kafka.
        >>> ds = ray.data.read_datasource(
        ...     KafkaDatasource(
        ...         bootstrap_servers="localhost:9092",
        ...         topic="my_topic",
        ...         consumer_config={"auto.offset.reset": "earliest"},
        ...     )
        ... )
        >>> # Process the streaming data like any other dataset.
        >>> ds.map(lambda record: record["value"].decode("utf-8").upper()).show()
    """

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        *,
        group_id: Optional[str] = None,
        partitions: Optional[List[int]] = None,
        consumer_config: Optional[Dict[str, Any]] = None,
        poll_timeout: float = 1.0,
        message_batch_size: int = 1000,
    ):
        """Create a Kafka datasource.

        Args:
            bootstrap_servers: A comma-separated list of Kafka broker addresses,
                e.g., "host1:9092,host2:9092".
            topic: The Kafka topic to consume from.
            group_id: The consumer group ID. If not provided, a unique group ID
                will be generated for the job.
            partitions: A list of partitions to consume from. If None (default),
                all partitions will be discovered and consumed.
            consumer_config: A dictionary of Kafka consumer configurations.
                Common configurations:
                - "auto.offset.reset": "earliest" or "latest" (default).
                - "security.protocol": "SASL_SSL"
                - "sasl.mechanisms": "PLAIN"
                - "sasl.username": "my_user"
                - "sasl.password": "my_password"
            poll_timeout: The timeout in seconds for polling messages.
            message_batch_size: The maximum number of messages to include in
                each Ray Block.
        """
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._partitions = partitions
        self._consumer_config = consumer_config or {}
        self._poll_timeout = poll_timeout
        self._message_batch_size = message_batch_size

        # Set bootstrap servers
        self._consumer_config["bootstrap.servers"] = self._bootstrap_servers

        # Handle group.id
        if group_id:
            if (
                "group.id" in self._consumer_config
                and self._consumer_config["group.id"] != group_id
            ):
                raise ValueError(
                    f"The `group_id` parameter ({group_id}) does not match the "
                    f"'group.id' in `consumer_config` ({self._consumer_config['group.id']})."
                )
            self._consumer_config["group.id"] = group_id
        elif "group.id" not in self._consumer_config:
            job_id = ray.get_runtime_context().get_job_id()
            default_group_id = f"ray-data-kafka-{job_id}"
            self._consumer_config["group.id"] = default_group_id
            logger.info(f"'group.id' not set, using default: {default_group_id}")

    def estimate_inmemory_data_size(self) -> Optional[int]:
        # It's difficult to estimate the size for a streaming datasource.
        return None

    def get_read_tasks(self, parallelism: int) -> List[ReadTask]:
        consumer_config = self._consumer_config
        topic = self._topic
        partitions = self._partitions

        # If partitions are not specified, discover them automatically.
        if partitions is None:
            try:
                c = Consumer(consumer_config)
                metadata = c.list_topics(topic, timeout=5)
                c.close()
                if topic not in metadata.topics:
                    raise ValueError(f"Topic '{topic}' not found in Kafka.")
                partitions = list(metadata.topics[topic].partitions.keys())
                logger.info(f"Discovered partitions: {partitions}")
            except KafkaException as e:
                raise RuntimeError(
                    f"Failed to discover partitions for topic '{topic}': {e}"
                )

        num_partitions = len(partitions)
        num_tasks = num_partitions

        if parallelism > 0 and parallelism < num_partitions:
            num_tasks = parallelism
        elif parallelism > num_partitions:
            logger.warning(
                f"Requested parallelism {parallelism} is greater than the number "
                f"of partitions {num_partitions}. The number of read tasks will be "
                f"limited to {num_partitions}."
            )

        partition_groups = np.array_split(partitions, num_tasks)

        read_tasks = []

        def create_read_fn(partitions_for_task: List[int]):
            """Create a read function for a specific set of partitions."""

            def read_fn():
                return _read_kafka_task(
                    topic=topic,
                    partitions=partitions_for_task,
                    consumer_config=consumer_config,
                    poll_timeout=self._poll_timeout,
                    message_batch_size=self._message_batch_size,
                )

            return read_fn

        for group in partition_groups:
            partitions_for_task = group.tolist()
            if not partitions_for_task:
                continue

            # Pass partition info as input_files for metadata.
            input_files = [
                f"kafka://{self._topic}/partition={p}" for p in partitions_for_task
            ]
            metadata = BlockMetadata(
                num_rows=None,
                size_bytes=None,
                schema=None,
                input_files=input_files,
                exec_stats=None,
            )
            read_tasks.append(
                ReadTask(create_read_fn(partitions_for_task), metadata)
            )
        return read_tasks
