from redis.asyncio import Redis
from typing import Optional, List

from repositories.persons import AbstractCachePersonRepository
from core.config import app_settings
from models.persons import DetailedPerson, ListPerson
from models.base_models import BasePerson
from models.films import ListBaseFilm


class PersonsRedisRepository(AbstractCachePersonRepository):
    tag = "persons"

    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_person_by_id(self, person_id: str) -> Optional[DetailedPerson]:
        data = await self._redis.get(person_id)

        if not data:
            return None

        person = DetailedPerson.model_validate_json(data)
        return person

    async def save_person_by_id(self, person: DetailedPerson) -> None:
        await self._redis.set(person.id, person.model_dump_json(), app_settings.redis_cache_expire)

    async def get_persons(
        self, page_number: int, page_size: int, sort: Optional[str] = None, query: Optional[str] = None
    ) -> Optional[ListPerson]:

        key = self._generate_key(page_number, page_size, sort, query)
        data = await self._redis.get(key)

        if not data:
            return None

        persons = ListPerson.model_validate_json(data)
        return persons

    async def save_persons(
        self,
        page_number: int,
        page_size: int,
        persons: List[BasePerson],
        sort: Optional[str] = None,
        query: Optional[str] = None,
    ) -> None:

        persons = ListPerson(persons=persons)
        key = self._generate_key(page_number, page_size, sort, query)

        await self._redis.set(key, persons.model_dump_json(), app_settings.redis_cache_expire)

    async def get_films_by_person_id(self, person_id: str) -> Optional[ListBaseFilm]:
        key = self._generate_key(person_id)
        data = await self._redis.get(key)

        if not data:
            return None

        films = ListBaseFilm.model_validate_json(data)
        return films

    async def save_films_by_person_id(self, person_id: str, films: ListBaseFilm) -> None:
        key = self._generate_key(person_id)
        await self._redis.set(key, films.model_dump_json(), app_settings.redis_cache_expire)

    def _generate_key(self, *args) -> str:
        key = [self.tag]

        for item in args:
            if item is not None:
                key.append(str(item))

        return "-".join(key)
