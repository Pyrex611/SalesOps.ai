from functools import lru_cache

from pydantic import field_validator
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

    @field_validator('max_upload_mb')
    @classmethod
    def validate_max_upload_mb(cls, value: int) -> int:
        if value <= 0:
            raise ValueError('MAX_UPLOAD_MB must be greater than 0')
        return value

    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, value: str, info) -> str:
        env = (info.data.get('env') or 'development').lower()
        if env in {'production', 'prod'} and value == 'change-me-in-production':
            raise ValueError('SECRET_KEY must be overridden in production')
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
