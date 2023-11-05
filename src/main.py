from contextlib import asynccontextmanager

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from gunicorn.app.base import BaseApplication

from api.v1 import films, persons, genres
from core.config import app_settings
from db import elastic
from db import redis


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    redis.redis = Redis(host=app_settings.redis_host, port=app_settings.redis_port)
    elastic.es = AsyncElasticsearch(hosts=[f"http://{app_settings.elastic_host}:{app_settings.elastic_port}"])
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    lifespan=lifespan,
    title=app_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, fastapi_app, gunicorn_options=None):
        self.options = gunicorn_options or {}
        self.application = fastapi_app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


options = {
    "bind": "0.0.0.0:8000",
    "accesslog": "-",
    "errorlog": "-",
    "worker_class": "uvicorn.workers.UvicornWorker",
}

if __name__ == "__main__":
    StandaloneApplication(app, options).run()
