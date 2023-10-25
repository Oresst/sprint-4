from fastapi import Depends
from redis.asyncio import Redis

from functools import lru_cache

from repositories.films.redis.films import FilmsRedisRepository
from db.redis import get_redis


@lru_cache()
def get_films_redis_repo(redis: Redis = Depends(get_redis)) -> FilmsRedisRepository:
    return FilmsRedisRepository(redis)
