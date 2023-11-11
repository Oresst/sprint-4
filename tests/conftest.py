from typing import List, AsyncGenerator
import json

import asyncio
from aiohttp import ClientSession
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from settings import test_app_settings
from functional.test_data.movies_index import movies_settings, movies_mapping
from functional.test_data.movies_data import movies_data
from functional.test_data.genres_index import genres_settings, genres_mapping
from functional.test_data.genres_data import genres_data
from functional.test_data.persons_index import persons_settings, persons_mapping
from functional.test_data.persons_data import persons_data


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def get_es_bulk_query(data: List[dict], index: str, id_field: str):
    bulk_query = []
    for row in data:
        bulk_query.extend(
            [json.dumps({"index": {"_index": index, "_id": row[id_field]}}), json.dumps(row),]
        )
    return bulk_query


@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=f"http://{test_app_settings.elastic_host}:{test_app_settings.elastic_port}")

    await client.indices.create(index="movies", mappings=movies_mapping, settings=movies_settings)
    await client.indices.create(index="genres", mappings=genres_mapping, settings=genres_settings)
    await client.indices.create(index="persons", mappings=persons_mapping, settings=persons_settings)

    yield client

    await client.indices.delete(index="movies")
    await client.indices.delete(index="genres")
    await client.indices.delete(index="persons")

    await client.close()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def es_write_data(es_client: AsyncElasticsearch):
    # Записываем фильмы
    bulk_query = get_es_bulk_query(movies_data, "movies", "id")

    response = await es_client.bulk(operations=bulk_query, refresh=True)

    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")

    # Записываем жанры
    bulk_query = get_es_bulk_query(genres_data, "genres", "id")

    response = await es_client.bulk(operations=bulk_query, refresh=True)

    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")

    # Записываем персон
    bulk_query = get_es_bulk_query(persons_data, "persons", "id")

    response = await es_client.bulk(operations=bulk_query, refresh=True)

    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[ClientSession, None]:
    async with ClientSession(base_url=test_app_settings.service_url) as ac:
        yield ac
