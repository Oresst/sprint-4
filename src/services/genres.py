from fastapi import Depends

from functools import lru_cache
from typing import Optional, List

from repositories.genres import AbstractDbGenresRepository, AbstractCacheGenreRepository
from repositories.genres.elastic import get_genres_elastic_repo
from repositories.genres.redis import get_genre_redis_repo
from models.genres import Genre


class GenresService:
    def __init__(self, db: AbstractDbGenresRepository, cache: AbstractCacheGenreRepository):
        self._db = db
        self._cache = cache

    async def get_genre_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._cache.get_genre_by_id(genre_id)

        if genre is not None:
            return genre

        genre = await self._db.get_genre_by_id(genre_id)

        if genre is not None:
            await self._cache.save_genre_by_id(genre)

        return genre

    async def get_genres(self) -> List[Genre]:
        genres = await self._cache.get_genres()

        if genres is not None:
            return genres

        genres = await self._db.get_genres()

        if genres is not None:
            await self._cache.save_genres(genres)

        return genres


@lru_cache
def get_genres_service(
    es: AbstractDbGenresRepository = Depends(get_genres_elastic_repo),
    redis: AbstractCacheGenreRepository = Depends(get_genre_redis_repo),
) -> GenresService:
    return GenresService(es, redis)
