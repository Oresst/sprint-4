from aiohttp import ClientSession
import pytest

from settings import test_app_settings
from conftest import ac


@pytest.mark.asyncio
async def test_search(ac: ClientSession):

    url = test_app_settings.service_url + "/api/v1/films"
    query_data = {"search": "Star Wars"}

    async with ac.get(url, params=query_data) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 10
