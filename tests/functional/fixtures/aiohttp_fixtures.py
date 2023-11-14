import logging

import pytest
import aiohttp

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    LOGGER.info('AIOHTTP client open')
    yield session
    await session.close()
    LOGGER.info('AIOHTTP client closed')
