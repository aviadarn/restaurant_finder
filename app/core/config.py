from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Reservation Hunter AI"
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "sqlite+aiosqlite:///./reservation_hunter.db"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str | None = None
    app_secret_key: str = Field(default="change-me")
    session_encryption_key: str = Field(default="change-me-change-me-change-me-change-me")
    jwt_secret: str = Field(default="change-me-too")
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    twilio_from_number: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    telegram_bot_token: str | None = None
    push_webhook_url: str | None = None
    playwright_headless: bool = True
    playwright_user_data_dir: str = "/tmp/reservation-hunter-playwright"
    auto_booking_default_enabled: bool = False
    human_approval_required: bool = True
    scan_interval_seconds: int = 30
    max_provider_requests_per_minute: int = 20
    provider_request_timeout_seconds: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
