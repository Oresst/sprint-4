from fastapi import HTTPException
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError, BadRequestError

from repositories.films import AbstractDbFilmRepository
from models.films import DetailedFilm
from models.base_models import BaseFilm


class FilmsElasticRepository(AbstractDbFilmRepository):
    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get_film_by_id(self, film_id: str) -> DetailedFilm | None:
        try:
            doc = await self._elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        except BadRequestError:
            raise HTTPException(status_code=400, detail="Bad request")

        return DetailedFilm(**doc["_source"])

    async def get_film_genres(self, film_id: str) -> list[str] | None:
        try:
            doc = await self._elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        except BadRequestError:
            raise HTTPException(status_code=400, detail="Bad request")

        return doc["_source"]["genre"]

    async def get_films(
            self,
            page_number: int = 1,
            page_size: int = 10,
            sort: str | None = None,
            query: str | None = None,
            genre: str | None = None,
    ) -> list[BaseFilm]:

        sort_dict = {}
        query_dict = {"bool": {"filter": []}}

        if sort is not None:
            sort_dict[sort.replace("-", "")] = "desc" if sort.find("-") else "asc"

        if query is not None:
            query_dict["bool"]["filter"].append({"match": {"title": {"query": query}}})

        if genre is not None:
            query_dict["bool"]["filter"].append({"term": {"genre": {"value": genre, "case_insensitive": True}}})

        try:
            doc = await self._elastic.search(
                index="movies", query=query_dict, from_=(page_number - 1) * page_size, size=page_size, sort=sort_dict
            )
        except NotFoundError:
            return []
        except BadRequestError:
            raise HTTPException(status_code=400, detail="Bad request")

        films = []

        for film in doc["hits"]["hits"]:
            films.append(BaseFilm(**film["_source"]))

        return films
