from fastapi import Depends, APIRouter

from typing import List

from services.genres import get_genres_service, GenresService
from models.genres import Genre

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def genre(genre_id: str, genres_service: GenresService = Depends(get_genres_service)) -> Genre:
    genre_item = await genres_service.get_genre_by_id(genre_id)
    return genre_item


@router.get("/", response_model=List[Genre])
async def genres_list(genres_service: GenresService = Depends(get_genres_service)) -> List[Genre]:
    genres = await genres_service.get_genres()
    return genres
