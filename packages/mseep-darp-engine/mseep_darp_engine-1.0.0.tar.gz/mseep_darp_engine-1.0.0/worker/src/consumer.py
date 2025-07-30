from datetime import timedelta
from typing import Any

from aiokafka import AIOKafkaConsumer

from .deployment_service import WorkerDeploymentService
from registry.src.database import get_unmanaged_session
from registry.src.logger import logger
from registry.src.servers.repository import ServerRepository
from registry.src.settings import settings
from worker.src.schemas import Task
from worker.src.schemas import TaskType


class Consumer:
    def __init__(self) -> None:
        self.max_poll_interval: int = int(timedelta(minutes=30).total_seconds())
        self.session_timeout: int = int(timedelta(minutes=10).total_seconds())
        self.task_handlers: dict[TaskType, Any] = {
            TaskType.deploy: self.deploy_server,
            TaskType.start: self.start_server,
            TaskType.stop: self.stop_server,
        }

    async def start(self) -> None:
        consumer = AIOKafkaConsumer(
            settings.worker_topic,
            bootstrap_servers=settings.broker_url,
            auto_offset_reset="earliest",
            group_id="deploy_workers",
            group_instance_id="1",
            max_poll_interval_ms=self.max_poll_interval * 1000,
            session_timeout_ms=self.session_timeout * 1000,
        )
        await consumer.start()
        try:
            await self.process_messages(consumer)
        finally:
            await consumer.stop()

    async def process_messages(self, consumer: AIOKafkaConsumer) -> None:
        async for message in consumer:
            incoming_message = self.parse_message(message.value)
            if not incoming_message:
                continue
            await self.process_message(incoming_message)

    async def process_message(self, task: Task) -> None:
        session = await get_unmanaged_session()
        try:
            repo = ServerRepository(session)
            await self.task_handlers[task.task_type](task.server_id, repo)
        except Exception as error:
            logger.error("Error while processing a task", exc_info=error)
        await session.commit()

    async def deploy_server(self, server_id: int, repo: ServerRepository) -> None:
        service = WorkerDeploymentService(repo=repo, logger=logger)
        await service.deploy_server(server_id=server_id)

    async def stop_server(self, server_id: int, repo: ServerRepository) -> None:
        raise NotImplementedError()

    async def start_server(self, server_id: int, repo: ServerRepository) -> None:
        raise NotImplementedError()

    @staticmethod
    def parse_message(message: bytes) -> Task | None:
        logger.debug(f"Incoming message - {message.decode()}")
        try:
            task = Task.model_validate_json(message.decode())
            return task
        except Exception as error:
            logger.error("Incorrect message received", exc_info=error)
            return None
