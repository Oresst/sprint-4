from redis.asyncio import Redis
from typing import Optional, List

from repositories.persons import AbstractCachePersonRepository
from core.config import app_settings
from models.persons import DetailedPerson, ListPerson, Person


class PersonsRedisRepository(AbstractCachePersonRepository):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_person_by_id(self, person_id: str) -> Optional[DetailedPerson]:
        data = await self._redis.get(person_id)

        if not data:
            return None

        person = DetailedPerson.model_validate_json(data)
        return person

    async def save_person_by_id(self, person: DetailedPerson) -> None:
        await self._redis.set(person.id, person.model_dump_json(), app_settings.person_cache_expire)

    async def get_persons(
            self, sort: Optional[str], query: Optional[str], genre: Optional[str], page_number: int, page_size: int
    ) -> Optional[ListPerson]:

        key = self._generate_key("persons", sort, query, genre, page_number, page_size)
        data = await self._redis.get(key)

        if not data:
            return None

        persons = ListPerson.model_validate_json(data)
        return persons

    async def save_persons(
            self,
            sort: Optional[str],
            query: Optional[str],
            genre: Optional[str],
            page_number: int,
            page_size: int,
            persons: List[Person],
    ) -> None:

        persons = ListPerson(persons=persons)
        key = self._generate_key("persons", sort, query, genre, page_number, page_size)

        await self._redis.set(key, persons.model_dump_json(), app_settings.person_cache_expire)

    @staticmethod
    def _generate_key(name: str, *args) -> str:
        key = [name]

        for item in args:
            if item is not None:
                key.append(str(item))

        return "-".join(key)
