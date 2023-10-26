from fastapi import Depends
from elasticsearch import AsyncElasticsearch

from functools import lru_cache

from db.elastic import get_elastic
from repositories.genres.elastic.genres import GenresElasticRepository


@lru_cache()
def get_genres_elastic_repo(elastic: AsyncElasticsearch = Depends(get_elastic)) -> GenresElasticRepository:
    return GenresElasticRepository(elastic)
