from fastapi import Depends
from redis.asyncio import Redis

from functools import lru_cache

from repositories.genres.redis.genres import GenresRedisRepository
from db.redis import get_redis


@lru_cache
def get_genre_redis_repo(redis: Redis = Depends(get_redis)) -> GenresRedisRepository:
    return GenresRedisRepository(redis)
