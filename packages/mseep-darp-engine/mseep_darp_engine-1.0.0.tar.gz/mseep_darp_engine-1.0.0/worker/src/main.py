import asyncio

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

from registry.src.logger import logger
from registry.src.settings import settings
from worker.src.consumer import Consumer


if __name__ == "__main__":
    try:
        admin = KafkaAdminClient(bootstrap_servers=settings.broker_url)

        worker_topic = NewTopic(
            name=settings.worker_topic, num_partitions=1, replication_factor=1
        )
        admin.create_topics([worker_topic])
    except TopicAlreadyExistsError:
        pass

    consumer = Consumer()
    logger.info("Starting consumer")
    asyncio.run(consumer.start())
