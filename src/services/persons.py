from fastapi import Depends

from functools import lru_cache

from models.persons import DetailedPerson
from models.base_models import BaseFilm
from repositories.persons import AbstractDbPersonRepository, AbstractCachePersonRepository
from repositories.persons.redis import get_persons_redis_repo
from repositories.persons.elastic import get_persons_elastic_repo


class PersonsService:
    def __init__(self, redis_repo: AbstractCachePersonRepository, elastic_repo: AbstractDbPersonRepository):
        self._cache = redis_repo
        self._db = elastic_repo

    async def get_person_by_id(self, person_id: str) -> DetailedPerson | None:
        person = await self._cache.get_person_by_id(person_id)

        if person is not None:
            return person

        person = await self._db.get_person_by_id(person_id)

        if person is not None:
            await self._cache.save_person_by_id(person)

        return person

    async def get_persons(
        self, page_number: int, page_size: int, sort: str | None = None, query: str | None = None
    ) -> list[DetailedPerson]:
        persons = await self._cache.get_persons(page_number, page_size, sort=sort, query=query)

        if persons is not None:
            return persons.persons

        persons = await self._db.get_persons(page_number, page_size, sort=sort, query=query)

        if persons:
            await self._cache.save_persons(page_number, page_size, persons, sort=sort, query=query)

        return persons

    async def get_films_by_person_id(self, person_id: str) -> list[BaseFilm]:
        films = await self._cache.get_films_by_person_id(person_id)

        if films is not None:
            return films.films

        films = await self._db.get_films_by_person_id(person_id)

        if films:
            await self._cache.save_films_by_person_id(person_id, films)

        return films.films


@lru_cache()
def get_persons_service(
    redis_repo: AbstractCachePersonRepository = Depends(get_persons_redis_repo),
    es_repo: AbstractDbPersonRepository = Depends(get_persons_elastic_repo),
) -> PersonsService:
    return PersonsService(redis_repo, es_repo)
