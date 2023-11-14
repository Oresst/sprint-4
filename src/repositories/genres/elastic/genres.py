from fastapi import HTTPException
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError, BadRequestError

from repositories.genres import AbstractDbGenresRepository
from models.genres import Genre


class GenresElasticRepository(AbstractDbGenresRepository):
    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        try:
            doc = await self._elastic.get(index="genres", id=genre_id)
        except NotFoundError:
            return None
        except BadRequestError:
            raise HTTPException(status_code=400, detail="Bad request")

        return Genre(**doc["_source"])

    async def get_genres(self) -> list[Genre]:
        try:
            doc = await self._elastic.search(index="genres", size=1000)
        except NotFoundError:
            return []
        except BadRequestError:
            raise HTTPException(status_code=400, detail="Bad request")

        genres = []

        for genre in doc["hits"]["hits"]:
            genres.append(Genre(**genre["_source"]))

        return genres
