from pydantic import BaseModel, Field
from typing import List, Optional


class Person(BaseModel):
    id: str = Field(serialization_alias="uuid")
    name: str = Field(serialization_alias="full_name")


class PersonFilms(BaseModel):
    id: str = Field(serialization_alias="uuid")
    roles: List[str]


class DetailedPerson(Person):
    films: List[PersonFilms]


class ListPerson(BaseModel):
    films: List[Person]
