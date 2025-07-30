from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CommandResult
from .schemas import CommandStart
from .schemas import GeneralLogMessage
from .schemas import LoggingEvent
from .schemas import LogLevel
from .schemas import LogMessage
from registry.src.deployments.logs_repository import LogsRepository


class UserLogger:

    def __init__(self, session: AsyncSession, server_id: int):
        self.logs_repo = LogsRepository(session=session)
        self.server_id = server_id

    async def clear_logs(self) -> None:
        await self.logs_repo.clear_logs(server_id=self.server_id)

    async def command_start(self, command: str) -> None:
        log = LogMessage(
            event_type=LoggingEvent.command_start, data=CommandStart(command=command)
        )
        await self.logs_repo.append_to_deployment_logs(
            server_id=self.server_id, log=log
        )

    async def command_result(self, output: str, success: bool) -> None:
        data = CommandResult(output=output, success=success)
        log = LogMessage(event_type=LoggingEvent.command_result, data=data)
        await self.logs_repo.append_to_deployment_logs(
            server_id=self.server_id, log=log
        )

    async def info(self, message: str) -> None:
        await self._add_message(log_level=LogLevel.info, message=message)

    async def warning(self, message: str) -> None:
        await self._add_message(log_level=LogLevel.warning, message=message)

    async def error(self, message: str) -> None:
        await self._add_message(log_level=LogLevel.error, message=message)

    async def _add_message(self, log_level: LogLevel, message: str):
        data = GeneralLogMessage(log_level=log_level, message=message)
        log = LogMessage(event_type=LoggingEvent.general_message, data=data)
        await self.logs_repo.append_to_deployment_logs(
            server_id=self.server_id, log=log
        )
