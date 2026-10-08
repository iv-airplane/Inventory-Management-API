from pydantic_settings import BaseSettings

# Application configuration.
# `database_url` defaults to a local SQLite file so the app runs with zero
# setup.
# `settings` below is instantiated once at import time and shared across the
# app (see app/core/database.py) rather than re-read per request.
class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./app.db"
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
