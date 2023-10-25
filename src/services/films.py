from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import Depends

from typing import Optional, List
from functools import lru_cache

from models.films import DetailedFilm, BaseFilm, ListBaseFilm
from core.config import app_settings
from db.redis import get_redis
from db.elastic import get_elastic


class FilmsService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self._redis = redis
        self._elastic = elastic

    async def get_film_by_id(self, film_id: str) -> Optional[DetailedFilm]:
        film = await self._get_film_by_id_from_cache(film_id)

        if film is not None:
            return film

        film = await self._get_film_by_id_from_elastic(film_id)

        if film is not None:
            await self._put_film_to_cache(film)

        return film

    async def get_films(
        self, sort: Optional[str], query: Optional[str], page_number: int, page_size: int
    ) -> List[BaseFilm]:
        films = await self._get_films_from_cache(page_number, page_size)

        if films is not None:
            return films.films

        films = await self._get_films_from_elastic(sort, query, page_number, page_size)

        if films is not None:
            await self._put_films_to_cache(page_number, page_size, films)

        return films

    async def _get_film_by_id_from_elastic(self, film_id: str) -> Optional[DetailedFilm]:
        try:
            doc = await self._elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return DetailedFilm(**doc["_source"])

    async def _get_films_from_elastic(
        self, sort: Optional[str], query: Optional[str], page_size: int, page_number: int
    ) -> Optional[List[BaseFilm]]:
        sort_dict = {}
        query_dict = {}

        if sort is not None:
            sort_dict[sort.replace("-", "")] = "desc" if sort.find("-") else "asc"

        if query is not None:
            query_dict = {"match": {"title": {"query": query}}}

        try:
            doc = await self._elastic.search(
                index="movies", query=query_dict, from_=page_number - 1, size=page_size, sort=sort_dict
            )
        except NotFoundError:
            return None

        films = []

        for film in doc["hits"]["hits"]:
            films.append(BaseFilm(**film["_source"]))

        return films

    async def _get_film_by_id_from_cache(self, film_id: str) -> Optional[DetailedFilm]:
        data = await self._redis.get(film_id)

        if not data:
            return None

        film = DetailedFilm.model_validate_json(data)
        return film

    async def _get_films_from_cache(self, page_number: int, page_size: int) -> Optional[ListBaseFilm]:
        data = await self._redis.get(f"films-{page_number}-{page_size}")

        if not data:
            return None

        films = ListBaseFilm.model_validate_json(data)
        return films

    async def _put_film_to_cache(self, film: DetailedFilm):
        await self._redis.set(film.id, film.model_dump_json(), app_settings.film_cache_expire)

    async def _put_films_to_cache(self, page_number: int, page_size: int, films: List[BaseFilm]):
        films = ListBaseFilm(films=films)
        await self._redis.set(
            f"films-{page_number}-{page_size}", films.model_dump_json(), app_settings.film_cache_expire
        )


@lru_cache()
def get_films_service(redis: Redis = Depends(get_redis), es: AsyncElasticsearch = Depends(get_elastic)) -> FilmsService:
    return FilmsService(redis, es)
