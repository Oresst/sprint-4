from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from typing import Optional, List

from repositories.persons import AbstractDbPersonRepository
from models.persons import DetailedPerson
from models.films import ListBaseFilm


class PersonsElasticRepository(AbstractDbPersonRepository):
    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get_person_by_id(self, person_id: str) -> Optional[DetailedPerson]:
        try:
            doc = await self._elastic.get(index="persons", id=person_id)
        except NotFoundError:
            return None
        return DetailedPerson(**doc["_source"])

    async def get_persons(
        self, page_number: int, page_size: int, sort: Optional[str] = None, query: Optional[str] = None
    ) -> List[DetailedPerson]:
        sort_dict = {}
        query_dict = {"bool": {"filter": []}}

        if sort is not None:
            sort_dict[sort.replace("-", "")] = "desc" if sort.find("-") else "asc"

        if query is not None:
            query_dict["bool"]["filter"].append({"match": {"full_name": {"query": query}}})

        try:
            doc = await self._elastic.search(
                index="persons", query=query_dict, from_=(page_number - 1) * page_size, size=page_size, sort=sort_dict
            )
        except NotFoundError:
            return []

        persons = []

        for person in doc["hits"]["hits"]:
            persons.append(DetailedPerson(**person["_source"]))

        return persons

    async def get_films_by_person_id(self, person_id: str) -> ListBaseFilm:
        try:
            doc = await self._elastic.get(index="persons", id=person_id)
        except NotFoundError:
            return ListBaseFilm(films=[])

        return ListBaseFilm(**doc["_source"])
