import asyncio
import logging

import redis
import pytest
import aiohttp
from yarl import URL
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from settings import test_settings
from utils.helpers import es_generate_actions, es_index_rows_generator

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = redis.Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    LOGGER.info('Redis client open')
    yield client
    del client
    LOGGER.info('Redis client closed')


@pytest.fixture(scope='session')
def redis_reset(redis_client: redis.Redis):
    def inner():
        redis_client.flushdb()
        LOGGER.info('Redis cache cleared')

    return inner


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_url, verify_certs=False)
    LOGGER.info('ES client open')
    yield client
    await client.close()
    LOGGER.info('ES client closed')


@pytest.fixture(scope="class")
def es_index_create(es_client: AsyncElasticsearch):
    async def inner(index_map: dict, index_name: str):
        if not await es_client.indices.exists(index=index_name):
            LOGGER.info(f'ES index "{index_name}" created')
            await es_client.indices.create(index=index_name, **index_map)

    return inner


@pytest.fixture(scope="class")
def es_index_remove(es_client: AsyncElasticsearch):
    async def inner(index_name: str):
        if await es_client.indices.exists(index=index_name):
            await es_client.indices.delete(index=index_name)
            LOGGER.info(f'ES index "{index_name}" deleted')

    return inner


@pytest.fixture(scope="class")
def clear_db_data(es_index_remove, redis_reset):
    async def inner(index_name: str):
        await es_index_remove(index_name)
        redis_reset()

    return inner


@pytest.fixture(scope="class")
def es_write_data(es_client: AsyncElasticsearch, es_index_create):
    async def inner(index_name: str, index_map: dict, rows_cnt: int = 1):
        await es_index_create(index_map, index_name)
        data = es_index_rows_generator(index_name, rows_cnt)
        bulk_data = es_generate_actions(index_name, data)
        success, errors = await async_bulk(es_client, bulk_data)
        LOGGER.info(f'Written into ES: success {success}, errors {len(errors)}')
        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

        return success, errors

    return inner


@pytest.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(aiohttp_session: aiohttp.ClientSession):
    async def inner(endpoint: str, query_data: dict):
        url = URL(test_settings.service_url + endpoint)
        async with aiohttp_session.get(url, params=query_data, ssl=False) as response:
            body = await response.json()
            return response, body

    return inner
