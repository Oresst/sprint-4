from functools import lru_cache

from fastapi import Depends

from models.films import DetailedFilm
from models.base_models import BaseFilm
from repositories.films.redis import get_films_redis_repo
from repositories.films.elastic import get_films_elastic_repo
from repositories.films import AbstractDbFilmRepository, AbstractCacheFilmRepository


class FilmsService:
    def __init__(self, cache: AbstractCacheFilmRepository, db: AbstractDbFilmRepository):
        self._cache = cache
        self._db = db

    async def get_film_by_id(self, film_id: str) -> DetailedFilm | None:
        film = await self._cache.get_film_by_id(film_id)

        if film is not None:
            return film

        film = await self._db.get_film_by_id(film_id)

        if film is not None:
            await self._cache.save_film_by_id(film)

        return film

    async def get_films(
            self,
            page_number: int = 1,
            page_size: int = 50,
            sort: str | None = None,
            query: str | None = None,
            genre: str | None = None,
    ) -> list[BaseFilm]:

        films = await self._cache.get_films(page_number, page_size, sort=sort, query=query, genre=genre)

        if films is not None:
            return films.films

        films = await self._db.get_films(page_number, page_size, sort=sort, query=query, genre=genre)

        if films:
            await self._cache.save_films(page_number, page_size, films, sort=sort, query=query, genre=genre)

        return films

    async def get_alike_films(self, film_id: str) -> list[BaseFilm] | None:
        films = await self._cache.get_alike_films(film_id)

        if films is not None:
            return films

        genres = await self._db.get_film_genres(film_id)

        if genres is None:
            return None

        films = await self._db.get_films(genre=genres[0])

        await self._cache.save_alike_films(film_id, films)

        return films


@lru_cache()
def get_films_service(
        cache: AbstractCacheFilmRepository = Depends(get_films_redis_repo),
        db: AbstractDbFilmRepository = Depends(get_films_elastic_repo),
) -> FilmsService:
    return FilmsService(cache, db)
