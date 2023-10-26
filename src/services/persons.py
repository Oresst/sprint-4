from fastapi import Depends

from typing import Optional, List
from functools import lru_cache

from models.persons import DetailedPerson, Person
from repositories.persons import AbstractDbPersonRepository, AbstractCachePersonRepository
from repositories.persons.redis import get_persons_redis_repo
from repositories.persons.elastic import get_persons_elastic_repo


class PersonsService:
    def __init__(self, redis_repo: AbstractCachePersonRepository, elastic_repo: AbstractDbPersonRepository):
        self._cache = redis_repo
        self._db = elastic_repo

    async def get_person_by_id(self, person_id: str) -> Optional[DetailedPerson]:
        person = await self._cache.get_person_by_id(person_id)

        if person is not None:
            return person

        person = await self._db.get_person_by_id(person_id)

        if person is not None:
            await self._cache.save_person_by_id(person)

        return person

    async def get_persons(
            self, sort: Optional[str], query: Optional[str], page_number: int, page_size: int
    ) -> List[DetailedPerson]:
        persons = await self._cache.get_persons(sort, query, page_number, page_size)

        if persons is not None:
            return persons.persons

        persons = await self._db.get_persons(sort, query, page_number, page_size)

        if persons is not None:
            await self._cache.save_persons(sort, query, page_number, page_size, persons)

        return persons


@lru_cache()
def get_persons_service(
        redis_repo: AbstractCachePersonRepository = Depends(get_persons_redis_repo),
        es_repo: AbstractDbPersonRepository = Depends(get_persons_elastic_repo),
) -> PersonsService:
    return PersonsService(redis_repo, es_repo)
