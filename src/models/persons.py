from pydantic import BaseModel, Field
from typing import List
from models.films import FilmRoles


class BasePerson(BaseModel):
    id: str = Field(serialization_alias="uuid")
    name: str = Field(serialization_alias="full_name")


class DetailedPerson(BasePerson):
    films: List[FilmRoles]


class ListPerson(BaseModel):
    persons: List[DetailedPerson]
