import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration settings.
    Variables are loaded from environment variables or .env file.
    """
    VIMEO_ACCESS_TOKEN: str
    VIMEO_BASE_URL: str = "https://api.vimeo.com"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra environment variables
        case_sensitive=True
    )

settings = Settings()
