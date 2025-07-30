from typing import Literal

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status as status_codes
from fastapi_pagination import add_pagination
from fastapi_pagination import Page
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..deployments.service import DeploymentService
from ..errors import InvalidData
from .schemas import MCPJson
from .schemas import ServerCreate
from .schemas import ServerRead
from .schemas import ServerUpdate
from .schemas import ServerWithTools
from .service import ServerService
from registry.src.database import get_session
from registry.src.database import Server
from registry.src.search.schemas import SearchServer
from registry.src.search.service import SearchService
from registry.src.types import RoutingMode
from registry.src.types import ServerStatus

router = APIRouter(prefix="/servers")
add_pagination(router)


@router.post(
    "/", response_model=ServerWithTools, status_code=status_codes.HTTP_201_CREATED
)
async def create(
    data: ServerCreate, service: ServerService = Depends(ServerService.get_new_instance)
) -> Server:
    return await service.create(data)


@router.get("/search", response_model=list[ServerWithTools])
async def search(
    query: str,
    routing_mode: RoutingMode = RoutingMode.auto,
    service: ServerService = Depends(ServerService.get_new_instance),
    search_service: SearchService = Depends(SearchService.get_new_instance),
) -> list[Server]:
    if routing_mode == RoutingMode.auto:
        servers = await service.get_search_servers()
        formatted_servers = [SearchServer.model_validate(server) for server in servers]
        server_urls = await search_service.get_fitting_servers(
            servers=formatted_servers, query=query
        )
        return await service.get_servers_by_urls(server_urls=server_urls)
    elif routing_mode == RoutingMode.deepresearch:
        return await service.get_deep_research()
    raise InvalidData(f"Unsupported {routing_mode=}", routing_mode=routing_mode)


@router.get("/batch", response_model=list[ServerWithTools])
async def get_servers_by_ids(
    ids: list[int] = Query(...),
    service: ServerService = Depends(ServerService.get_new_instance),
) -> list[Server]:
    return await service.get_servers_by_ids(ids=ids)


@router.get("/.well-known/mcp.json", response_model=MCPJson)
async def get_mcp_json(
    service: ServerService = Depends(ServerService.get_new_instance),
) -> MCPJson:
    return await service.get_mcp_json()


@router.delete("/{id}")
async def delete_server(
    id: int,
    current_user_id: str,
    service: ServerService = Depends(ServerService.get_new_instance),
) -> None:
    return await service.delete_server(id=id, current_user_id=current_user_id)


@router.get("/", response_model=Page[ServerWithTools])
async def get_all_servers(
    query: str | None = None,
    status: Literal["any"] | ServerStatus = Query(
        title="Server status",
        default=ServerStatus.active,
        description="Filter servers by status, by default servers with status `active` will be returned",
    ),
    creator_id: str | None = None,
    params: Params = Depends(),
    service: ServerService = Depends(ServerService.get_new_instance),
    session: AsyncSession = Depends(get_session),
) -> Page[Server]:
    status_filter: ServerStatus | None = None

    if isinstance(status, ServerStatus):
        status_filter = status

    servers: Select = await service.get_all_servers(
        search_query=query,
        status=status_filter,
        creator_id=creator_id,
    )
    return await paginate(session, servers, params)


@router.get("/{id}", response_model=ServerWithTools)
async def get_server_by_id(
    id: int,
    service: ServerService = Depends(ServerService.get_new_instance),
) -> Server:
    return await service.get_server_by_id(id=id)


@router.put("/{id}", response_model=ServerRead)
async def update_server(
    id: int,
    data: ServerUpdate,
    service: ServerService = Depends(ServerService.get_new_instance),
    deployment_service: DeploymentService = Depends(DeploymentService.get_new_instance),
) -> Server:
    await deployment_service.update_deployment(server_id=id, data=data)
    server = await service.update_server(id=id, data=data)
    return server
