from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str


@lru_cache()
def get_settings():
    return Settings()
