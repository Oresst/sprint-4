from fastapi import Depends
from elasticsearch import AsyncElasticsearch

from functools import lru_cache

from db.elastic import get_elastic
from repositories.films.elastic.films import FilmsElasticRepository


@lru_cache()
def get_films_elastic_repo(elastic: AsyncElasticsearch = Depends(get_elastic)) -> FilmsElasticRepository:
    return FilmsElasticRepository(elastic)
