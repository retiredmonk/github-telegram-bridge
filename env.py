from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GITHUB_TOKEN: str
    TELEGRAM_TOKEN: str
    CHAT_ID: str
    OWNER: str
    REPO: str
    POLL_INTERVAL: int

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()