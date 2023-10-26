from fastapi import APIRouter, Depends

from typing import List, Optional

from models.persons import DetailedPerson, BasePerson
from services.persons import get_persons_service, PersonsService

router = APIRouter()


@router.get("/{person_id}", response_model=DetailedPerson)
async def person_details(person_id: str, persons_service: PersonsService = Depends(get_persons_service)) -> DetailedPerson:
    person = await persons_service.get_person_by_id(person_id)
    return person


@router.get("/", response_model=List[BasePerson])
async def person_details(
    sort: Optional[str] = None,
    query: Optional[str] = None,
    genre: Optional[str] = None,
    page_size: int = 10,
    page_number: int = 1,
    persons_service: PersonsService = Depends(get_persons_service),
) -> List[BasePerson]:
    person = await persons_service.get_persons(sort, query, genre, page_size, page_number)
    return person
