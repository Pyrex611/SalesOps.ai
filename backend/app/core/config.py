from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'SalesOps.ai'
    env: str = 'development'
    secret_key: str = 'change-me-in-production'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60
    database_url: str = 'sqlite+aiosqlite:///./salesops.db'
    cors_origins: str = 'http://localhost:3000'
    max_upload_mb: int = 500
    storage_path: str = './storage'


@lru_cache

def get_settings() -> Settings:
    return Settings()
