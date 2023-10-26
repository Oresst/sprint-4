from pydantic import BaseModel, Field
from typing import List, Optional


class Person(BaseModel):
    id: str = Field(serialization_alias="uuid")
    name: str = Field(serialization_alias="full_name")


class BasePerson(BaseModel):
    id: str = Field(serialization_alias="uuid")
    full_name: str


class PersonFilms(BaseModel):
    id: str = Field(serialization_alias="uuid")
    imdb_rating: float
    title: str
    roles: List[str]


class DetailedPerson(BasePerson):
    films: List[PersonFilms]


class ListPerson(BaseModel):
    persons: List[DetailedPerson]
