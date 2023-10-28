from fastapi import Depends, APIRouter, HTTPException

from typing import List

from services.genres import get_genres_service, GenresService
from services.films import get_films_service, FilmsService
from models.genres import Genre
from models.base_models import BaseFilm

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def genre(genre_id: str, genres_service: GenresService = Depends(get_genres_service)) -> Genre:
    genre_item = await genres_service.get_genre_by_id(genre_id)

    if genre_item is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre_item


@router.get("/", response_model=List[Genre])
async def genres_list(genres_service: GenresService = Depends(get_genres_service)) -> List[Genre]:
    genres = await genres_service.get_genres()
    return genres


@router.get("/{genre_name}/popular", response_model=List[BaseFilm])
async def popular_films_in_genre(
    genre_name: str, films_service: FilmsService = Depends(get_films_service)
) -> List[BaseFilm]:
    films = await films_service.get_films(genre=genre_name, sort="imdb_rating")
    return films
