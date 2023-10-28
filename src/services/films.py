from fastapi import Depends

from typing import Optional, List
from functools import lru_cache

from models.films import DetailedFilm, BaseFilm
from repositories.films import AbstractDbFilmRepository, AbstractCacheFilmRepository
from repositories.films.redis import get_films_redis_repo
from repositories.films.elastic import get_films_elastic_repo


class FilmsService:
    def __init__(self, redis_repo: AbstractCacheFilmRepository, elastic_repo: AbstractDbFilmRepository):
        self._cache = redis_repo
        self._db = elastic_repo

    async def get_film_by_id(self, film_id: str) -> Optional[DetailedFilm]:
        film = await self._cache.get_film_by_id(film_id)

        if film is not None:
            return film

        film = await self._db.get_film_by_id(film_id)

        if film is not None:
            await self._cache.save_film_by_id(film)

        return film

    async def get_films(
        self, sort: Optional[str], query: Optional[str], genre: Optional[str], page_number: int, page_size: int
    ) -> List[BaseFilm]:
        films = await self._cache.get_films(sort, query, genre, page_number, page_size)

        if films is not None:
            return films.films

        films = await self._db.get_films(sort, query, genre, page_number, page_size)

        if films:
            await self._cache.save_films(sort, query, genre, page_number, page_size, films)

        return films


@lru_cache()
def get_films_service(
    redis_repo: AbstractCacheFilmRepository = Depends(get_films_redis_repo),
    es_repo: AbstractDbFilmRepository = Depends(get_films_elastic_repo),
) -> FilmsService:
    return FilmsService(redis_repo, es_repo)
