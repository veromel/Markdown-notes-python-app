from pydantic import BaseSettings
from typing import List
from pydantic import AnyUrl


class Settings(BaseSettings):
    mongodb_url: AnyUrl
    allow_origins: List[str]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
