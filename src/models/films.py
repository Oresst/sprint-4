from pydantic import BaseModel, Field

from typing import List, Optional

from models.persons import Person


class BaseFilm(BaseModel):
    id: str = Field(serialization_alias="uuid")
    title: str
    imdb_rating: float


class DetailedFilm(BaseFilm):
    description: Optional[str]
    actors: List[Person]
    writers: List[Person]
    director: List[str] = Field(serialization_alias="directors")


class ListBaseFilm(BaseModel):
    films: List[BaseFilm]
