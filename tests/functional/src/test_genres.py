from random import choice

from aiohttp import ClientSession
import pytest

from conftest import ac
from functional.test_data.genres_data import genres_data
from functional.test_data.movies_data import movies_data


@pytest.mark.asyncio
async def test_get_genre_200(ac: ClientSession):
    genre = choice(genres_data)
    genre["uuid"] = genre.pop("id")

    async with ac.get("/api/v1/genres/{0}".format(genre["uuid"])) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert body == genre


@pytest.mark.asyncio
async def test_get_genre_404(ac: ClientSession):
    async with ac.get("/api/v1/genres/biuOIGByo") as response:
        status = response.status

    assert status == 404


@pytest.mark.asyncio
async def test_get_all_genres(ac: ClientSession):
    async with ac.get("/api/v1/genres") as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(genres_data) == len(body)


@pytest.mark.asyncio
async def test_get_popular_films_by_genre(ac: ClientSession):
    genre = choice(genres_data)

    async with ac.get("/api/v1/genres/{0}/popular".format(genre["name"])) as response:
        body = await response.json()
        status = response.status

    assert status == 200

    films_uuids = {item["uuid"] for item in body}

    for film in movies_data:
        if film["id"] in films_uuids:
            assert genre["name"] in film["genre"]


@pytest.mark.asyncio
async def test_get_popular_films_by_wrong_genre(ac: ClientSession):
    async with ac.get("/api/v1/genres/{0}/popular".format("nvilsahu")) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert body == []
