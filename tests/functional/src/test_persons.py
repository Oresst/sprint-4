from random import choice

from aiohttp import ClientSession
import pytest

from conftest import ac
from functional.test_data.persons_data import persons_data


@pytest.mark.asyncio
async def test_get_person_200(ac: ClientSession):
    person = choice(persons_data)
    person["uuid"] = person.pop("id")

    async with ac.get("/api/v1/persons/{0}".format(person["uuid"])) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert body["uuid"] == person["uuid"]
    assert body["full_name"] == person["full_name"]
    assert len(body["films"]) == len(person["films"])


@pytest.mark.asyncio
async def test_get_person_404(ac: ClientSession):
    async with ac.get("/api/v1/persons/alndfiuaoruh") as response:
        status = response.status

    assert status == 404


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page_number": 1, "page_size": 10}, {"status": 200, "length": 10}),
        ({"page_number": 1, "page_size": 20}, {"status": 200, "length": 20}),
        ({"page_number": 100, "page_size": 20}, {"status": 200, "length": 0}),
    ],
)
@pytest.mark.asyncio
async def test_get_persons_pagination(ac: ClientSession, query_data, expected_answer):
    async with ac.get("/api/v1/persons", params=query_data) as response:
        body = await response.json()
        status = response.status

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "Victoria"}, {"status": 200, "length": 1}),
        ({"query": "Karl Genus"}, {"status": 200, "length": 1}),
        ({"query": "Some Name"}, {"status": 200, "length": 0}),
    ],
)
@pytest.mark.asyncio
async def test_get_persons_search(ac: ClientSession, query_data, expected_answer):
    async with ac.get("/api/v1/persons", params=query_data) as response:
        body = await response.json()
        status = response.status

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.asyncio
async def test_get_films_by_person(ac: ClientSession):
    person = choice(persons_data)

    async with ac.get("/api/v1/persons/{0}/film".format(person["id"])) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == len(person["films"])


@pytest.mark.asyncio
async def test_get_films_by_wrong_person(ac: ClientSession):
    async with ac.get("/api/v1/persons/cniaovniuo/film") as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert body == []
