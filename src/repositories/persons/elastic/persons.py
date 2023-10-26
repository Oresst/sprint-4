from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from typing import Optional, List

from repositories.persons import AbstractDbPersonRepository
from models.persons import DetailedPerson, Person


class PersonsElasticRepository(AbstractDbPersonRepository):
    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get_persons_by_id(self, persons_id: str) -> Optional[DetailedPerson]:
        try:
            doc = await self._elastic.get(index="movies", id=persons_id)
        except NotFoundError:
            return None
        return DetailedPerson(**doc["_source"])

    async def get_persons(
            self, sort: Optional[str], query: Optional[str], genre: Optional[str], page_size: int, page_number: int
    ) -> Optional[List[Person]]:
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
            return None

        persons = []

        for persons in doc["hits"]["hits"]:
            persons.append(Person(**persons["_source"]))

        return persons
