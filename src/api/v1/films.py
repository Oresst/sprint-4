from fastapi import APIRouter, Depends, HTTPException

from http import HTTPStatus
from models.films import DetailedFilm
from models.base_models import BaseFilm
from services.films import get_films_service, FilmsService

router = APIRouter()


@router.get("/{film_id}", response_model=DetailedFilm)
async def film_details(film_id: str, films_service: FilmsService = Depends(get_films_service)) -> DetailedFilm:
    film = await films_service.get_film_by_id(film_id)

    if film is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")

    return film


@router.get("/", response_model=list[BaseFilm])
async def films_list(
        page_number: int = 1,
        page_size: int = 10,
        films_service: FilmsService = Depends(get_films_service),
        sort: str | None = None,
        query: str | None = None,
        genre: str | None = None,
) -> list[BaseFilm]:
    film = await films_service.get_films(page_number, page_size, sort=sort, query=query, genre=genre)

    return film


@router.get("/{film_id}/alike", response_model=list[BaseFilm])
async def alike_films(film_id: str, films_service: FilmsService = Depends(get_films_service)) -> list[BaseFilm]:
    film = await films_service.get_alike_films(film_id)

    if film is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film id not found")

    return film
