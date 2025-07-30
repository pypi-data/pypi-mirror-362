from aiokafka import AIOKafkaProducer

from registry.src.settings import settings


async def get_producer(url=settings.broker_url) -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=url,
        value_serializer=lambda m: m.model_dump_json().encode("utf-8"),
    )
