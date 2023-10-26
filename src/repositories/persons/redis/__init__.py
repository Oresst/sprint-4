from fastapi import Depends
from redis.asyncio import Redis

from functools import lru_cache

from repositories.persons.redis.persons import PersonsRedisRepository
from db.redis import get_redis


@lru_cache()
def get_persons_redis_repo(redis: Redis = Depends(get_redis)) -> PersonsRedisRepository:
    return PersonsRedisRepository(redis)
