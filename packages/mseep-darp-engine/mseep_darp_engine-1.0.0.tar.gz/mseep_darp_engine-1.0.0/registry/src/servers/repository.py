from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy import Select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .schemas import ServerCreateData
from .schemas import ServerUpdateData
from .schemas import Tool
from registry.src.database import get_session
from registry.src.database import Server
from registry.src.database import Tool as DBTool
from registry.src.deployments.schemas import DeploymentCreateData
from registry.src.errors import ServersNotFoundError
from registry.src.types import ServerStatus
from registry.src.types import ServerTransportProtocol
from worker.src.constants import BaseImage


class ServerRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_servers(
        self,
        id: int | None = None,
        name: str | None = None,
        url: str | None = None,
        ignore_id: int | None = None,
        repo_url: str | None = None,
    ) -> list[Server]:
        if id is None and name is None and url is None:
            raise ValueError("At least one of 'id', 'name', or 'url' must be provided.")
        if id == ignore_id and id is not None:
            raise ValueError("id and ignore_id cannot be the same.")

        query = select(Server).options(selectinload(Server.tools))
        conditions = [
            (Server.id == id),
            (func.lower(Server.name) == func.lower(name)),
        ]
        if url:
            conditions.append(Server.url == url)
        if repo_url:
            conditions.append(Server.repo_url == repo_url)
        query = query.filter(or_(*conditions))
        query = query.filter(Server.id != ignore_id)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_server(self, id: int) -> Server:
        query = select(Server).filter(Server.id == id)
        query = query.options(selectinload(Server.tools))
        result = await self.session.execute(query)
        server = result.scalars().first()
        if server is None:
            raise ServersNotFoundError([id])
        return server

    async def create_server(
        self,
        data: ServerCreateData | DeploymentCreateData,
        tools: list[Tool],
        creator_id: str | None,
        transport_protocol: ServerTransportProtocol | None = None,
    ) -> Server:
        db_tools = []
        if isinstance(data, ServerCreateData):
            db_tools = self._convert_tools(tools, data.url)
        server = Server(
            **data.model_dump(exclude_none=True),
            tools=db_tools,
            creator_id=creator_id,
            transport_protocol=transport_protocol,
        )
        self.session.add(server)
        await self.session.flush()
        await self.session.refresh(server)
        return await self.get_server(server.id)

    async def get_all_servers(
        self,
        search_query: str | None = None,
        status: ServerStatus | None = None,
        creator_id: str | None = None,
    ) -> Select:
        query = select(Server).options(selectinload(Server.tools))

        if status is not None:
            query = query.where(Server.status == status)

        if creator_id:
            query = query.where(Server.creator_id == creator_id)

        if search_query:
            query_string = f"%{search_query}%"
            query = query.where(
                or_(
                    Server.name.ilike(query_string),
                    Server.description.ilike(query_string),
                    Server.title.ilike(query_string),
                )
            )
        return query

    async def get_servers_by_urls(self, urls: list[str]) -> list[Server]:
        query = select(Server).where(Server.url.in_(urls))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_servers_by_ids(self, ids: list[int]) -> list[Server]:
        query = (
            select(Server).where(Server.id.in_(ids)).options(selectinload(Server.tools))
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def delete_server(self, id: int) -> None:
        query = delete(Server).where(Server.id == id)
        await self.session.execute(query)

    async def update_server(
        self,
        id: int,
        data: ServerUpdateData | None = None,
        tools: list[Tool] | None = None,
        status: ServerStatus | None = None,
        repo_url: str | None = None,
        command: str | None = None,
        base_image: BaseImage | None = None,
        build_instructions: str | None = None,
        transport_protocol: ServerTransportProtocol | None = None,
    ) -> Server:
        server = await self.get_server(id)
        update_values = dict(
            status=status,
            repo_url=repo_url,
            command=command,
            transport_protocol=transport_protocol,
            base_image=base_image,
            build_instructions=build_instructions,
        )
        update_values = {
            key: value for key, value in update_values.items() if value is not None
        }
        if data:
            update_values.update(data.model_dump(exclude_none=True))
        for key, value in update_values.items():
            setattr(server, key, value)

        if tools is not None:
            query = delete(DBTool).where(DBTool.server_url == server.url)
            await self.session.execute(query)
            await self.session.flush()
            await self.session.refresh(server)
            server.tools.extend(self._convert_tools(tools, server.url))

        await self.session.flush()
        await self.session.refresh(server)
        return server

    def _convert_tools(self, tools: list[Tool], url: str) -> list[DBTool]:
        return [
            DBTool(**tool.model_dump(exclude_none=True), server_url=url)
            for tool in tools
        ]

    @classmethod
    def get_new_instance(
        cls, session: AsyncSession = Depends(get_session)
    ) -> "ServerRepository":
        return cls(session)
