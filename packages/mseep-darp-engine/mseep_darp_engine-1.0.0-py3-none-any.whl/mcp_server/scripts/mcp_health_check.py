import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client

from mcp_server.src.settings import settings


async def healthcheck():
    async with sse_client(f"http://localhost:{settings.mcp_port}/sse") as (
        read,
        write,
    ):
        async with ClientSession(read, write) as session:
            await session.initialize()


if __name__ == "__main__":
    asyncio.run(healthcheck())
