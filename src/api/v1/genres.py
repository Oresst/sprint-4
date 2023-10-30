from http import HTTPStatus

from fastapi import Depends, APIRouter, HTTPException

from models.genres import Genre
from models.base_models import BaseFilm
from services.films import get_films_service, FilmsService
from services.genres import get_genres_service, GenresService

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def genre(genre_id: str, genres_service: GenresService = Depends(get_genres_service)) -> Genre:
    genre_item = await genres_service.get_genre_by_id(genre_id)

    if genre_item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")

    return genre_item


@router.get("/", response_model=list[Genre])
async def genres_list(genres_service: GenresService = Depends(get_genres_service)) -> list[Genre]:
    genres = await genres_service.get_genres()
    return genres


@router.get("/{genre_name}/popular", response_model=list[BaseFilm])
async def popular_films_in_genre(
        genre_name: str, films_service: FilmsService = Depends(get_films_service)
) -> list[BaseFilm]:
    films = await films_service.get_films(genre=genre_name, sort="imdb_rating")
    return films
