from pydantic import BaseModel, Field


class BaseFilm(BaseModel):
    id: str = Field(serialization_alias="uuid")
    title: str
    imdb_rating: float


class BasePerson(BaseModel):
    id: str = Field(serialization_alias="uuid")
    name: str = Field(alias="full_name")

    class Config:
        populate_by_name = True
