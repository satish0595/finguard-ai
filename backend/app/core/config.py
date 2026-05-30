"""Application settings (Pydantic v2)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "FinGuard AI"
    app_env: str = "development"
    debug: bool = True

    database_url: str = (
        "postgresql+asyncpg://finguard:finguard@localhost:5432/finguard"
    )
    database_url_sync: str = (
        "postgresql+psycopg2://finguard:finguard@localhost:5432/finguard"
    )

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30


settings = Settings()
