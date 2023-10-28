from redis.asyncio import Redis
from typing import Optional, List

from repositories.films import AbstractCacheFilmRepository
from core.config import app_settings
from models.films import DetailedFilm, ListBaseFilm
from models.base_models import BaseFilm


class FilmsRedisRepository(AbstractCacheFilmRepository):
    tag = "films"

    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_film_by_id(self, film_id: str) -> Optional[DetailedFilm]:
        data = await self._redis.get(film_id)

        if not data:
            return None

        film = DetailedFilm.model_validate_json(data)
        return film

    async def save_film_by_id(self, film: DetailedFilm) -> None:
        await self._redis.set(film.id, film.model_dump_json(), app_settings.redis_cache_expire)

    async def get_films(
        self,
        page_number: int,
        page_size: int,
        sort: Optional[str] = None,
        query: Optional[str] = None,
        genre: Optional[str] = None,
    ) -> Optional[ListBaseFilm]:

        key = self._generate_key(page_number, page_size, sort, query, genre)
        data = await self._redis.get(key)

        if not data:
            return None

        films = ListBaseFilm.model_validate_json(data)
        return films

    async def save_films(
        self,
        page_number: int,
        page_size: int,
        films: List[BaseFilm],
        sort: Optional[str] = None,
        query: Optional[str] = None,
        genre: Optional[str] = None,
    ) -> None:

        films = ListBaseFilm(films=films)
        key = self._generate_key(page_number, page_size, sort, query, genre)

        await self._redis.set(key, films.model_dump_json(), app_settings.redis_cache_expire)

    async def get_alike_films(self, film_id: str) -> Optional[List[BaseFilm]]:
        key = self._generate_key("alike", film_id)

        data = await self._redis.get(key)

        if not data:
            return None

        films = ListBaseFilm.model_validate_json(data)
        return films.films

    async def save_alike_films(self, film_id: str, films: List[BaseFilm]) -> None:
        key = self._generate_key("alike", film_id)

        films = ListBaseFilm(films=films)

        await self._redis.set(key, films.model_dump_json(), app_settings.redis_cache_expire)

    def _generate_key(self, *args) -> str:
        key = [self.tag]

        for item in args:
            if item is not None:
                key.append(str(item))

        return "-".join(key)
