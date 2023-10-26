from pydantic_settings import BaseSettings
from pydantic import Field

import os
from logging import config as logging_config

from logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    project_name: str = Field(default="movies", validation_alias="PROJECT_NAME")
    redis_host: str = Field(default="127.0.0.1", validation_alias="REDIS_HOST")
    redis_port: int = Field(default=6379, validation_alias="REDIS_PORT")
    elastic_host: str = Field(default="127.0.0.1", validation_alias="ELASTIC_HOST")
    elastic_port: int = Field(default=9200, validation_alias="ELASTIC_PORT")

    film_cache_expire: int = Field(default=60 * 5)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app_settings = AppSettings()
