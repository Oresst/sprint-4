import logging

import pytest
from elasticsearch import AsyncElasticsearch

from settings import test_settings as settings

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='session', params=[{'hosts': settings.es_url, 'verify_certs': False}])
async def es_client(request):
    client = AsyncElasticsearch(**request.param)
    LOGGER.info('ES client open')
    yield client
    await client.close()
    LOGGER.info('ES client closed')


@pytest.fixture(scope="class")
def es_index_create(es_client: AsyncElasticsearch):
    async def inner(index_name: str, index_attributes: dict):
        if not await es_client.indices.exists(index=index_name):
            LOGGER.info(f'ES index "{index_name}" created')
            await es_client.indices.create(index=index_name, **index_attributes)

    return inner


@pytest.fixture(scope="class")
def es_index_remove(es_client: AsyncElasticsearch):
    async def inner(index_name: str):
        if await es_client.indices.exists(index=index_name):
            await es_client.indices.delete(index=index_name)
            LOGGER.info(f'ES index "{index_name}" deleted')

    return inner
