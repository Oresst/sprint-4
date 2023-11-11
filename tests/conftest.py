from typing import List
import json

import asyncio
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from settings import test_app_settings
from functional.test_data.movies_index import movies_settings, movies_mapping
from functional.test_data.movies_data import movies_data


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

    yield client

    await client.indices.delete(index="movies")

    await client.close()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def es_write_data(es_client: AsyncElasticsearch):
    # Записываем фильмы
    bulk_query = get_es_bulk_query(movies_data, "movies", "id")

    response = await es_client.bulk(operations=bulk_query, refresh=True)
    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")
