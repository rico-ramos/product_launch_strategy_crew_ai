from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_model_name: str = "gpt-4o-mini"
    tavily_api_key: str

    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    storage_dir: str = "storage/runs"
    frontend_api_base: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
