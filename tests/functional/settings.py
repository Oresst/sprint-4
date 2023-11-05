import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str = Field(default='127.0.0.1', validation_alias='REDIS_HOST')
    redis_port: int = Field(default=6379, validation_alias='REDIS_PORT')
    es_url: str = Field(default='http://127.0.0.1:9200', validation_alias='ELASTIC_URL')
    service_url: str = Field(default='http://127.0.0.1:8001', validation_alias='SERVICE_URL')

    redis_cache_expire: int = Field(default=60 * 5)

    model_config = SettingsConfigDict(
        env_file='env/local.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
test_settings = Settings()
