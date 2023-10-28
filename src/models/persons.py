from pydantic import BaseModel

from typing import List

from models.films import FilmRoles
from models.base_models import BasePerson


class DetailedPerson(BasePerson):
    films: List[FilmRoles]


class ListPerson(BaseModel):
    persons: List[DetailedPerson]
