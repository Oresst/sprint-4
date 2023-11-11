import aiohttp
import pytest

from settings import test_app_settings


@pytest.mark.asyncio
async def test_search():
    session = aiohttp.ClientSession()

    url = test_app_settings.service_url + "/api/v1/films"
    query_data = {"search": "Star Wars"}

    async with session.get(url, params=query_data) as response:
        body = await response.json()
        status = response.status

    await session.close()

    assert status == 200
    assert len(body) == 10
