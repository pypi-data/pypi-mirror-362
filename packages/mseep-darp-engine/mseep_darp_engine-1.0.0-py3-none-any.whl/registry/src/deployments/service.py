import re
from typing import Self

from fastapi import Depends

from ..settings import settings
from ..types import HostType
from ..types import TaskType
from .logs_repository import LogsRepository
from .schemas import DeploymentCreate
from registry.src.database import Server
from registry.src.database import ServerLogs
from registry.src.errors import InvalidData
from registry.src.errors import InvalidServerNameError
from registry.src.errors import NotAllowedError
from registry.src.errors import ServerAlreadyExistsError
from registry.src.errors import ServersNotFoundError
from registry.src.producer import get_producer
from registry.src.servers.repository import ServerRepository
from registry.src.servers.schemas import ServerRead
from registry.src.servers.schemas import ServerUpdate
from registry.src.servers.service import ID_REGEX_PATTERN
from registry.src.types import ServerStatus
from worker.src.schemas import Task


class DeploymentService:
    def __init__(self, repo: ServerRepository, logs_repo: LogsRepository) -> None:
        self.repo = repo
        self.logs_repo = logs_repo

    async def get_server(self, server_id: int, creator_id: str | None = None) -> Server:
        await self._assure_server_found(server_id)
        server = await self.repo.get_server(server_id)
        if creator_id:
            await self._assure_server_creator(server=server, user_id=creator_id)
        return server

    async def get_logs(self, server_id: int, current_user_id: str) -> ServerLogs:
        server = await self.get_server(server_id=server_id, creator_id=current_user_id)
        if server.host_type != HostType.internal:
            raise InvalidData("Logs are only available for internal servers")
        logs = await self.logs_repo.get_server_logs(server_id=server_id)
        assert logs
        return logs

    async def create_server(self, data: DeploymentCreate) -> Server:
        self._assure_server_name_is_valid_id(data.data.name)
        await self._assure_server_not_exists(
            name=data.data.name, repo_url=str(data.data.repo_url)
        )
        server = await self.repo.create_server(
            data=data.data, creator_id=data.current_user_id, tools=[]
        )
        await self.logs_repo.create_logs(server_id=server.id)
        await self.repo.session.commit()
        await self._send_task(server_id=server.id, task_type=TaskType.deploy)
        return server

    async def update_deployment(self, server_id: int, data: ServerUpdate) -> Server:
        server = await self.get_server(
            server_id=server_id, creator_id=data.current_user_id
        )
        if not data.deployment_data.model_dump(exclude_none=True):
            return server
        server = await self.repo.update_server(
            id=server_id,
            **data.deployment_data.model_dump(),
            status=ServerStatus.in_processing,
        )
        await self.repo.session.commit()
        await self._send_task(server_id=server.id, task_type=TaskType.deploy)
        return server

    async def stop_server(self, server_id: int, current_user_id: str) -> None:
        server = await self.get_server(server_id=server_id, creator_id=current_user_id)
        if server.status == ServerStatus.stopped:
            return
        if server.status != ServerStatus.active:
            raise InvalidData("Server is not active", server_status=server.status)
        await self._send_task(server_id=server_id, task_type=TaskType.stop)

    async def start_server(self, server_id: int, current_user_id: str) -> None:
        server = await self.get_server(server_id=server_id, creator_id=current_user_id)
        if server.status == ServerStatus.active:
            return
        if server.status != ServerStatus.stopped:
            raise InvalidData("Invalid server state", server_status=server.status)
        await self._send_task(server_id=server_id, task_type=TaskType.start)

    @staticmethod
    async def _send_task(server_id: int, task_type: TaskType) -> None:
        producer = await get_producer()
        await producer.start()
        await producer.send_and_wait(
            topic=settings.worker_topic,
            value=Task(task_type=task_type, server_id=server_id),
        )
        await producer.stop()

    async def _assure_server_found(self, server_id: int) -> None:
        if not await self.repo.find_servers(id=server_id):
            raise ServersNotFoundError([server_id])

    @staticmethod
    async def _assure_server_creator(server: Server, user_id: str) -> None:
        if server.creator_id != user_id:
            raise NotAllowedError(
                "Must be server creator to use this function",
                creator_id=server.creator_id,
                current_user_id=user_id,
            )

    async def _assure_server_not_exists(
        self,
        name: str | None = None,
        repo_url: str | None = None,
        ignore_id: int | None = None,
    ) -> None:
        if servers := await self.repo.find_servers(
            name=name, repo_url=repo_url, ignore_id=ignore_id
        ):
            dict_servers = [
                ServerRead.model_validate(server).model_dump() for server in servers
            ]
            raise ServerAlreadyExistsError(dict_servers)

    @staticmethod
    def _assure_server_name_is_valid_id(name: str) -> None:
        if not re.match(ID_REGEX_PATTERN, name):
            raise InvalidServerNameError(name=name)

    @classmethod
    def get_new_instance(
        cls,
        repo: ServerRepository = Depends(ServerRepository.get_new_instance),
        logs_repo: LogsRepository = Depends(LogsRepository.get_new_instance),
    ) -> Self:
        return cls(repo=repo, logs_repo=logs_repo)
