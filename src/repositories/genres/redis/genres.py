from redis.asyncio import Redis

from typing import Optional, List

from core.config import app_settings
from repositories.genres import AbstractCacheGenreRepository
from models.genres import Genre, GenreList


class GenresRedisRepository(AbstractCacheGenreRepository):
    tag = "genres"

    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_genre_by_id(self, genre_id: str) -> Optional[Genre]:
        data = await self._redis.get(genre_id)

        if not data:
            return None

        genre = Genre.model_validate_json(data)
        return genre

    async def save_genre_by_id(self, genre: Genre) -> None:
        await self._redis.set(genre.uuid, genre.model_dump_json(), app_settings.redis_cache_expire)

    async def get_genres(self) -> Optional[List[Genre]]:
        data = await self._redis.get(self.tag)

        if not data:
            return None

        genres = GenreList.model_validate_json(data)
        return genres.genres

    async def save_genres(self, genres: List[Genre]) -> None:
        genres_list = GenreList(genres=genres)

        await self._redis.set(self.tag, genres_list.model_dump_json(), app_settings.redis_cache_expire)
