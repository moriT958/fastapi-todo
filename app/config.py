from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str

    # model_config = SettingsConfigDict(env_file="../.env")  # 本番環境ではこの記述は不要
    


@lru_cache()
def get_settings():
    return Settings()