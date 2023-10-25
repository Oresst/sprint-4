from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from typing import Optional, List

from repositories.films import AbstractDbFilmRepository
from models.films import DetailedFilm, BaseFilm


class FilmsElasticRepository(AbstractDbFilmRepository):
    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get_film_by_id(self, film_id: str) -> Optional[DetailedFilm]:
        try:
            doc = await self._elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return DetailedFilm(**doc["_source"])

    async def get_films(
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
