from pydantic import BaseModel, Field

from models.base_models import BasePerson, BaseFilm


class FilmRoles(BaseModel):
    id: str = Field(serialization_alias="uuid")
    roles: list[str]


class DetailedFilm(BaseFilm):
    description: str | None
    actors: list[BasePerson]
    writers: list[BasePerson]
    director: list[str] = Field(serialization_alias="directors")


class ListBaseFilm(BaseModel):
    films: list[BaseFilm]
