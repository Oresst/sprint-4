from aiohttp import ClientSession
import pytest

from conftest import ac


@pytest.mark.asyncio
async def test_search(ac: ClientSession):
    query_data = {"search": "Star Wars"}

    async with ac.get("/api/v1/films", params=query_data) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 10
