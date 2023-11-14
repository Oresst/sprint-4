import asyncio
import logging

import pytest
import aiohttp
from yarl import URL
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from settings import test_settings
from testdata import index_data_map, index_attributes_map
from utils.helpers import es_generate_actions

pytest_plugins = (
    "fixtures.redis_fixtures",
    "fixtures.es_fixtures",
    'fixtures.aiohttp_fixtures',
)

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="class")
def clear_db_data(es_index_remove, redis_reset):
    async def inner(index_name: str):
        await es_index_remove(index_name)
        redis_reset()

    return inner


@pytest.fixture(scope="class")
def es_write_data(es_client: AsyncElasticsearch, es_index_create):
    async def inner(index_name: str):
        await es_index_create(index_name, index_attributes_map[index_name])
        data = index_data_map[index_name]
        bulk_data = es_generate_actions(index_name, data)
        success, errors = await async_bulk(es_client, bulk_data)
        LOGGER.info(f'Written into ES: success {success}, errors {len(errors)}')
        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

        return success, errors

    return inner


@pytest.fixture
def make_get_request(aiohttp_session: aiohttp.ClientSession):
    async def inner(endpoint: str, query_data: dict):
        url = URL(test_settings.service_url + endpoint)
        async with aiohttp_session.get(url, params=query_data, ssl=False) as response:
            body = await response.json()
            return response, body

    return inner
