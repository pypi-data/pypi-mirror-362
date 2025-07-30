import re
from contextlib import _AsyncGeneratorContextManager  # noqa
from typing import Self

from fastapi import Depends
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from pydantic import ValidationError
from sqlalchemy import Select

from ..settings import settings
from .repository import ServerRepository
from .schemas import MCP
from .schemas import MCPJson
from .schemas import ServerCreate
from .schemas import ServerRead
from .schemas import ServerUpdate
from .schemas import Tool
from .schemas import tool_name_regex
from registry.src.database import Server
from registry.src.errors import InvalidData
from registry.src.errors import InvalidServerNameError
from registry.src.errors import NotAllowedError
from registry.src.errors import RemoteServerError
from registry.src.errors import ServerAlreadyExistsError
from registry.src.errors import ServersNotFoundError
from registry.src.logger import logger
from registry.src.types import ServerStatus
from registry.src.types import ServerTransportProtocol

BASE_SERVER_NAME = "base_darp_server#REPLACEME"
ID_REGEX_PATTERN = re.compile(rf"^[a-zA-Z_][a-zA-Z0-9_]*|{BASE_SERVER_NAME}$")


class ServerService:
    def __init__(self, repo: ServerRepository) -> None:
        self.repo = repo

    async def create(self, data: ServerCreate) -> Server:
        self._assure_server_name_is_valid_id(data.data.name)
        await self._assure_server_not_exists(name=data.data.name, url=data.data.url)

        server_transport_protocol = await self.detect_transport_protocol(
            server_url=data.data.url
        )

        logger.info(
            "Detected server's transport protocol %s", server_transport_protocol
        )

        tools = await self.get_tools(
            server_url=data.data.url,
            server_name=data.data.name,
            transport=server_transport_protocol,
        )
        return await self.repo.create_server(
            data.data,
            tools,
            creator_id=data.current_user_id,
            transport_protocol=server_transport_protocol,
        )

    @classmethod
    async def get_tools(
        cls,
        server_url: str,
        server_name: str,
        transport: ServerTransportProtocol | None = None,
    ) -> list[Tool]:

        if transport is None:
            transport = await cls.detect_transport_protocol(server_url)

        try:
            return await cls._fetch_tools(
                server_url=server_url, server_name=server_name, transport=transport
            )
        except Exception as e:
            if isinstance(e, InvalidData):
                raise
            logger.warning(
                f"Error while getting tools from server {server_url}",
                exc_info=e,
            )
            raise InvalidData(
                "Server is unhealthy or URL does not lead to a valid MCP server",
                url=server_url,
            )

    async def delete_server(self, id: int, current_user_id: str) -> None:
        server = await self.get_server_by_id(id=id)
        if server.creator_id != current_user_id:
            raise NotAllowedError("Only server creator can delete it")
        await self.repo.delete_server(id=id)

    async def get_all_servers(
        self,
        status: ServerStatus | None = None,
        search_query: str | None = None,
        creator_id: str | None = None,
    ) -> Select:
        return await self.repo.get_all_servers(
            search_query=search_query, status=status, creator_id=creator_id
        )

    async def get_server_by_id(self, id: int) -> Server:
        await self._assure_server_found(id)
        return await self.repo.get_server(id=id)

    async def get_servers_by_ids(self, ids: list[int]) -> list[Server]:
        servers = await self.repo.get_servers_by_ids(ids=ids)
        if len(ids) != len(servers):
            retrieved_server_ids = {server.id for server in servers}
            missing_server_ids = set(ids) - retrieved_server_ids
            raise ServersNotFoundError(ids=list(missing_server_ids))
        return servers

    async def update_server(self, id: int, data: ServerUpdate) -> Server:
        server = await self.get_server_by_id(id=id)
        transport_protocol = None
        if server.creator_id != data.current_user_id:
            raise NotAllowedError("Only server creator can update it")
        if data.data.name or data.data.url:
            await self._assure_server_not_exists(
                name=data.data.name, url=data.data.url, ignore_id=id
            )
        updated_server_url = data.data.url or server.url
        if updated_server_url is not None:
            transport_protocol = await self.detect_transport_protocol(
                server_url=updated_server_url
            )
            tools = await self.get_tools(
                server_url=updated_server_url,
                server_name=data.data.name or server.name,
                transport=transport_protocol,
            )
        else:
            tools = []

        return await self.repo.update_server(
            id,
            data.data,
            tools,
            transport_protocol=transport_protocol,
        )

    async def _assure_server_found(self, id: int) -> None:
        if not await self.repo.find_servers(id=id):
            raise ServersNotFoundError([id])

    def _assure_server_name_is_valid_id(self, name: str) -> None:
        if not re.match(ID_REGEX_PATTERN, name):
            raise InvalidServerNameError(name=name)

    async def _assure_server_not_exists(
        self,
        id: int | None = None,
        name: str | None = None,
        url: str | None = None,
        ignore_id: int | None = None,
    ) -> None:
        if servers := await self.repo.find_servers(id, name, url, ignore_id):
            dict_servers = [
                ServerRead.model_validate(server).model_dump() for server in servers
            ]
            raise ServerAlreadyExistsError(dict_servers)

    async def get_search_servers(self) -> list[Server]:
        servers_query = await self.repo.get_all_servers()
        servers_query = servers_query.where(Server.url != None)  # noqa
        servers = (await self.repo.session.execute(servers_query)).scalars().all()
        return list(servers)

    async def get_servers_by_urls(self, server_urls: list[str]) -> list[Server]:
        servers = await self.repo.get_servers_by_urls(urls=server_urls)
        if len(server_urls) != len(servers):
            retrieved_server_urls = {server.url for server in servers}
            missing_server_urls = set(server_urls) - retrieved_server_urls
            logger.warning(
                f"One or more server urls are incorrect {missing_server_urls=}"
            )
        return servers

    async def get_mcp_json(self) -> MCPJson:
        servers = await self.repo.get_all_servers()
        servers = (await self.repo.session.execute(servers)).scalars().all()
        return MCPJson(servers=[MCP.model_validate(server) for server in servers])

    async def get_deep_research(self) -> list[Server]:
        servers = await self.repo.find_servers(name=settings.deep_research_server_name)
        if len(servers) == 0:
            raise RemoteServerError(
                f"{settings.deep_research_server_name} MCP server does not exist in registry"
            )
        assert len(servers) == 1, "Invalid state. Multiple deepresearch servers found"
        if servers[0].status != ServerStatus.active:
            raise RemoteServerError(
                f"{settings.deep_research_server_name} MCP server is down."
            )
        return servers

    @classmethod
    def get_new_instance(
        cls, repo: ServerRepository = Depends(ServerRepository.get_new_instance)
    ) -> Self:
        return cls(repo=repo)

    @classmethod
    async def _fetch_tools(
        cls, server_url: str, server_name: str, transport: ServerTransportProtocol
    ) -> list[Tool]:
        client_ctx = cls._get_client_context(server_url, transport)

        async with client_ctx as (read, write, *_):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_response = await session.list_tools()
        try:
            tools = [
                Tool(
                    **tool.model_dump(exclude_none=True),
                    alias=f"{tool.name}__{server_name}",
                )
                for tool in tools_response.tools
            ]
        except ValidationError:
            raise InvalidData(
                message=f"Invalid tool names. {{tool_name}}__{{server_name}} must fit {tool_name_regex}"
            )
        return tools

    @classmethod
    def _get_client_context(
        cls,
        server_url: str,
        transport_protocol: ServerTransportProtocol,
    ) -> _AsyncGeneratorContextManager:
        if transport_protocol == ServerTransportProtocol.STREAMABLE_HTTP:
            client_ctx = streamablehttp_client(server_url)
        elif transport_protocol == ServerTransportProtocol.SSE:
            client_ctx = sse_client(server_url)
        else:
            raise RuntimeError(
                "Unsupported transport protocol: %s", transport_protocol.name
            )

        return client_ctx

    @classmethod
    async def detect_transport_protocol(
        cls,
        server_url: str,
    ) -> ServerTransportProtocol:
        for protocol in (
            ServerTransportProtocol.STREAMABLE_HTTP,
            ServerTransportProtocol.SSE,
        ):
            if await cls._is_transport_supported(server_url, protocol):
                return protocol

        raise InvalidData(
            "Can't detect server's transport protocol, maybe server is unhealthy?",
            url=server_url,
        )

    @classmethod
    async def _is_transport_supported(
        cls,
        server_url: str,
        protocol: ServerTransportProtocol,
    ) -> bool:
        try:
            client_ctx = cls._get_client_context(server_url, protocol)
            async with client_ctx as (read, write, *_):
                return await cls._can_initialize_session(read, write)

        except Exception as e:
            logger.error(
                "Failed to create %s client",
                protocol.name,
                exc_info=e,
            )
            return False

    @staticmethod
    async def _can_initialize_session(read, write) -> bool:
        try:
            async with ClientSession(read, write) as session:
                await session.initialize()
            return True
        except Exception:
            return False
