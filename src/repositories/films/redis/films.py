from redis.asyncio import Redis
from typing import Optional, List

from repositories.films import AbstractCacheFilmRepository
from core.config import app_settings
from models.films import DetailedFilm, ListBaseFilm, BaseFilm


class FilmsRedisRepository(AbstractCacheFilmRepository):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_film_by_id(self, film_id: str) -> Optional[DetailedFilm]:
        data = await self._redis.get(film_id)

        if not data:
            return None

        film = DetailedFilm.model_validate_json(data)
        return film

    async def save_film_by_id(self, film: DetailedFilm) -> None:
        await self._redis.set(film.id, film.model_dump_json(), app_settings.film_cache_expire)

    async def get_films(self, page_number: int, page_size: int) -> Optional[ListBaseFilm]:
        data = await self._redis.get(f"films-{page_number}-{page_size}")

        if not data:
            return None

        films = ListBaseFilm.model_validate_json(data)
        return films

    async def save_films(self, page_number: int, page_size: int, films: List[BaseFilm]) -> None:
        films = ListBaseFilm(films=films)
        await self._redis.set(
            f"films-{page_number}-{page_size}", films.model_dump_json(), app_settings.film_cache_expire
        )
