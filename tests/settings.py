from pydantic import Field
from pydantic_settings import BaseSettings


class TestAppSettings(BaseSettings):
    redis_host: str = Field(default="127.0.0.1", validation_alias="REDIS_HOST")
    redis_port: int = Field(default=6379, validation_alias="REDIS_PORT")

    elastic_host: str = Field(default="127.0.0.1", validation_alias="ELASTIC_HOST")
    elastic_port: int = Field(default=9200, validation_alias="ELASTIC_PORT")

    service_url: str = Field("http://127.0.0.1:8000", validation_alias="SERVICE_URL")


test_app_settings = TestAppSettings()
