"""Application configuration from environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/draftvision"
    redis_url: str = "redis://localhost:6379/0"
    riot_api_key: str = ""
    riot_region: str = "br1"
    log_level: str = "INFO"
    use_memory_store: bool = False  # Set USE_MEMORY_STORE=true for tests


settings = Settings()
