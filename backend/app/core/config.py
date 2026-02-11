from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SalesOps.ai API"
    api_prefix: str = "/api/v1"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite+aiosqlite:///./salesops.db"
    transcription_provider: str = "deepgram"
    llm_provider: str = "gemini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
