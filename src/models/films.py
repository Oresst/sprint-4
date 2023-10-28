from pydantic import BaseModel, Field

from typing import List, Optional

from models.persons import BasePerson


class BaseFilm(BaseModel):
    id: str = Field(serialization_alias="uuid")
    title: str
    imdb_rating: float


class FilmRoles(BaseModel):
    id: str = Field(serialization_alias="uuid")
    roles: List[str]


class DetailedFilm(BaseFilm):
    description: Optional[str]
    actors: List[BasePerson]
    writers: List[BasePerson]
    director: List[str] = Field(serialization_alias="directors")


class ListBaseFilm(BaseModel):
    films: List[BaseFilm]
