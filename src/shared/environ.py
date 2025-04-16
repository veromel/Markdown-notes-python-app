from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    # MONGODB CONFIGURATION
    MONGODB_URL: str = "mongodb://localhost:27017"  # MongoDB connection URI
    MONGODB_NAME: str = "notes"
    allow_origins: List[str] = ["*"]

    HOST: str = "0.0.0.0"
    PORT: str = "8000"

    @classmethod
    def reload(cls) -> "Environment":
        """Reload environment from .env file"""
        return cls()


env = Environment()
