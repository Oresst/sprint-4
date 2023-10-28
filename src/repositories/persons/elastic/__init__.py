from fastapi import Depends
from elasticsearch import AsyncElasticsearch

from functools import lru_cache

from db.elastic import get_elastic
from repositories.persons.elastic.persons import PersonsElasticRepository


@lru_cache()
def get_persons_elastic_repo(elastic: AsyncElasticsearch = Depends(get_elastic)) -> PersonsElasticRepository:
    return PersonsElasticRepository(elastic)
