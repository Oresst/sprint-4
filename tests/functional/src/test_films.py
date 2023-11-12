from random import choice

from aiohttp import ClientSession
import pytest

from conftest import ac
from functional.test_data.movies_data import movies_data


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"search": "Star Wars"}, {"status": 200, "length": 10}),
        ({"search": "Star Wars", "page_size": 5}, {"status": 200, "length": 5}),
        ({"search": "Star Trek", "page_size": 30}, {"status": 200, "length": 30}),
        ({"genre": "Adventure", "page_size": 30}, {"status": 200, "length": 30}),
        ({"genre": "Adventure", "page_size": 30, "page_number": 2}, {"status": 200, "length": 9}),
    ],
)
@pytest.mark.asyncio
async def test_films_search(ac: ClientSession, query_data, expected_answer):
    async with ac.get("/api/v1/films", params=query_data) as response:
        body = await response.json()
        status = response.status

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.asyncio
async def test_get_movie_200(ac: ClientSession):
    movie = choice(movies_data).copy()
    movie["uuid"] = movie.pop("id")

    async with ac.get("/api/v1/films/{0}".format(movie["uuid"])) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert body["uuid"] == movie["uuid"]
    assert len(body["actors"]) == len(movie["actors"])
    assert len(body["writers"]) == len(movie["writers"])


@pytest.mark.asyncio
async def test_get_movie_404(ac: ClientSession):
    async with ac.get("/api/v1/films/ggngaiupe") as response:
        status = response.status

    assert status == 404


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page_number": 1, "page_size": 10}, {"status": 200, "length": 10}),
        ({"page_number": 1, "page_size": 50}, {"status": 200, "length": 50}),
        ({"page_number": 100, "page_size": 10}, {"status": 200, "length": 0}),
    ],
)
@pytest.mark.asyncio
async def test_get_films_pagination(ac: ClientSession, query_data, expected_answer):
    async with ac.get("/api/v1/films", params=query_data) as response:
        body = await response.json()
        status = response.status

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
