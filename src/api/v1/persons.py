from fastapi import APIRouter, Depends, HTTPException

from typing import List, Optional

from models.persons import DetailedPerson
from models.base_models import BaseFilm
from services.persons import get_persons_service, PersonsService

router = APIRouter()


@router.get("/{person_id}", response_model=DetailedPerson)
async def person_details(
    person_id: str, persons_service: PersonsService = Depends(get_persons_service)
) -> DetailedPerson:
    person = await persons_service.get_person_by_id(person_id)

    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    return person


@router.get("/", response_model=List[DetailedPerson])
async def persons_list(
    page_number: int = 1,
    page_size: int = 10,
    persons_service: PersonsService = Depends(get_persons_service),
    sort: Optional[str] = None,
    query: Optional[str] = None,
) -> List[DetailedPerson]:
    person = await persons_service.get_persons(page_number, page_size, sort=sort, query=query)
    return person


@router.get("/{person_id}/film", response_model=List[BaseFilm])
async def persons_films(
    person_id: str, persons_service: PersonsService = Depends(get_persons_service)
) -> List[BaseFilm]:
    films = await persons_service.get_films_by_person_id(person_id)
    return films
