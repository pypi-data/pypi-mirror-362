from fastapi import FastAPI

from registry.src.deployments.router import router as deploy_router
from registry.src.servers.router import router as servers_router

app = FastAPI()

app.include_router(servers_router)
app.include_router(deploy_router)


@app.get("/healthcheck")
async def healthcheck():
    return "Alive"
