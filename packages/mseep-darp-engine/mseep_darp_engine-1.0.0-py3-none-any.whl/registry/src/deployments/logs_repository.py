from typing import Self

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from registry.src.database import get_session
from registry.src.database import ServerLogs
from worker.src.schemas import LogMessage


class LogsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_logs(self, server_id: int) -> ServerLogs:
        server_logs = ServerLogs(server_id=server_id)
        self.session.add(server_logs)
        await self.session.flush()
        await self.session.refresh(server_logs)
        return server_logs

    async def get_server_logs(self, server_id: int) -> ServerLogs | None:
        query = select(ServerLogs).where(ServerLogs.server_id == server_id)
        logs = (await self.session.execute(query)).scalar_one_or_none()
        return logs

    async def update_server_logs(
        self, server_id: int, deployment_logs: list[dict]
    ) -> None:
        query = (
            update(ServerLogs)
            .where(ServerLogs.server_id == server_id)
            .values(deployment_logs=deployment_logs)
        )
        await self.session.execute(query)
        await self.session.flush()
        await self.session.commit()

    async def append_to_deployment_logs(self, server_id: int, log: LogMessage) -> None:
        query = select(ServerLogs).where(ServerLogs.server_id == server_id)
        logs: ServerLogs = (await self.session.execute(query)).scalar_one_or_none()
        if not logs:
            raise ValueError
        deployment_logs = logs.deployment_logs + [log.model_dump()]
        await self.update_server_logs(
            server_id=server_id, deployment_logs=deployment_logs
        )

    async def clear_logs(self, server_id: int) -> None:
        await self.update_server_logs(server_id=server_id, deployment_logs=[])

    @classmethod
    async def get_new_instance(
        cls, session: AsyncSession = Depends(get_session)
    ) -> Self:
        return cls(session=session)
