import logging
from collections.abc import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from common.notifications.client import NotificationsClient
from registry.src.database.models.server import Server
from registry.src.servers.repository import ServerRepository
from registry.src.servers.schemas import Tool
from registry.src.servers.service import ServerService
from registry.src.types import ServerStatus


class HealthChecker:
    def __init__(
        self,
        session: AsyncSession,
        servers_repo: ServerRepository,
        notifications_client: NotificationsClient,
    ) -> None:
        self.session = session
        self.repo = servers_repo
        self.notifications_client = notifications_client
        self.logger = logging.getLogger("Healthchecker")

    async def run_once(self) -> None:
        servers = await self._fetch_servers()

        for server in servers:
            await self._check_server(server)

    async def _fetch_servers(self) -> Sequence[Server]:
        query: Select = await self.repo.get_all_servers()
        servers: Sequence[Server] = (
            (await self.session.execute(query)).scalars().fetchall()
        )
        return servers

    async def _get_tools(self, server: Server) -> list[Tool]:
        return await ServerService.get_tools(server.url, server.name)

    async def _check_server(self, server: Server) -> None:
        self.logger.info("Checking server %s", server.name)

        try:
            tools = await self._get_tools(server)
        except Exception as error:
            await self._handle_failed_server(server, error)
            return

        if not tools:
            await self._handle_empty_tools(server)
            return

        await self._mark_server_healthy(server, tools)

    async def _handle_failed_server(self, server: Server, error: Exception) -> None:
        self.logger.error("Failed to fetch server's tools", exc_info=error)
        self.logger.warning("Server %s will be marked as unhealthy", server.name)
        await self.notifications_client.send_server_down_alert(
            server.creator_id,
            server_name=server.name,
        )
        await self._update_server_status(server, [], ServerStatus.inactive)

    async def _handle_empty_tools(self, server: Server) -> None:
        self.logger.warning("Server %s is alive, but has no tools", server.name)
        self.logger.warning("Server will be marked as unhealthy.")
        await self.notifications_client.send_server_down_alert(
            server.creator_id,
            server_name=server.name,
            server_logs=(
                "Server has no tools. It will be marked as unhealthy. "
                "Please, check it out."
            ),
        )
        await self._update_server_status(server, [], ServerStatus.inactive)

    async def _mark_server_healthy(self, server: Server, tools: list[Tool]) -> None:
        await self._update_server_status(server, tools, ServerStatus.active)

    async def _update_server_status(
        self, server: Server, tools: list[Tool], status: ServerStatus
    ) -> None:
        await self.repo.update_server(
            id=server.id,
            tools=tools,
            status=status,
        )
