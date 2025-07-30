from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_ignore_empty=True)

    postgres_user: str
    postgres_db: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5432

    db_pool_size: int = 50
    db_max_overflow: int = 25
    log_dir: Path = Path("logs")
    llm_proxy: str | None = None
    openai_api_key: str
    llm_model: str = "openai/gpt-4o-mini"
    openai_base_url: str = "https://openrouter.ai/api/v1"

    worker_topic: str = "deployment"
    deployment_server: str = ""
    deployment_network: str = ""
    broker_url: str = "portal_kafka:19092"
    dockerhub_login: str = ""
    dockerhub_password: str = ""
    registry_url: str = "http://registry/"
    healthcheck_running_interval: int = 3600
    tool_retry_count: int = 60
    tool_wait_interval: int = 5

    deep_research_server_name: str = "deepresearch_darpserver"

    @property
    def database_url(self) -> str:
        auth_data = f"{self.postgres_user}:{self.postgres_password}"
        host = f"{self.postgres_host}:{self.postgres_port}"
        return f"{auth_data}@{host}/{self.postgres_db}"

    @property
    def database_url_sync(self) -> str:
        return f"postgresql+psycopg2://{self.database_url}"

    @property
    def database_url_async(self) -> str:
        return f"postgresql+asyncpg://{self.database_url}"


settings = Settings()
