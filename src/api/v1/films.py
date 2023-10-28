from fastapi import APIRouter, Depends, HTTPException

from typing import List, Optional

from models.films import DetailedFilm
from models.base_models import BaseFilm
from services.films import get_films_service, FilmsService

router = APIRouter()


@router.get("/{film_id}", response_model=DetailedFilm)
async def film_details(film_id: str, films_service: FilmsService = Depends(get_films_service)) -> DetailedFilm:
    film = await films_service.get_film_by_id(film_id)

    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")

    return film


@router.get("/", response_model=List[BaseFilm])
async def films_list(
    page_number: int = 1,
    page_size: int = 10,
    films_service: FilmsService = Depends(get_films_service),
    sort: Optional[str] = None,
    query: Optional[str] = None,
    genre: Optional[str] = None,
) -> List[BaseFilm]:

    film = await films_service.get_films(page_number, page_size, sort=sort, query=query, genre=genre)

    return film


@router.get("/{film_id}/alike", response_model=List[BaseFilm])
async def alike_films(film_id: str, films_service: FilmsService = Depends(get_films_service)) -> List[BaseFilm]:
    film = await films_service.get_alike_films(film_id)

    if film is None:
        raise HTTPException(status_code=404, detail="Film id not found")

    return film
