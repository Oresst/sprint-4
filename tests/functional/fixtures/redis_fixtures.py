import logging

import pytest
from redis.asyncio import Redis

from settings import test_settings as settings

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session", params=[{'host': settings.redis_host, 'port': settings.redis_port}])
async def redis_client(request):
    client = Redis(**request.param)
    LOGGER.info('Redis client open')
    yield client
    await client.aclose()
    LOGGER.info('Redis client closed')


@pytest.fixture(scope="session")
def redis_reset(redis_client: Redis):
    def inner():
        redis_client.flushdb()
        LOGGER.info('Redis cache cleared')

    return inner
