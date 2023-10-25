from fastapi import APIRouter, Depends

from typing import List, Optional

from models.films import DetailedFilm, BaseFilm
from services.films import get_films_service, FilmsService

router = APIRouter()


@router.get("/{film_id}", response_model=DetailedFilm)
async def film_details(film_id: str, films_service: FilmsService = Depends(get_films_service)) -> DetailedFilm:
    film = await films_service.get_film_by_id(film_id)
    return film


@router.get("/", response_model=List[BaseFilm])
async def film_details(
    sort: Optional[str],
    query: Optional[str],
    page_size: int = 10,
    page_number: int = 1,
    films_service: FilmsService = Depends(get_films_service),
) -> List[BaseFilm]:
    film = await films_service.get_films(sort, query, page_size, page_number)
    return film
