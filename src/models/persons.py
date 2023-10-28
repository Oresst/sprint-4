from pydantic import BaseModel

from models.films import FilmRoles
from models.base_models import BasePerson


class DetailedPerson(BasePerson):
    films: list[FilmRoles]


class ListPerson(BaseModel):
    persons: list[DetailedPerson]
