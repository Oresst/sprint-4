from pydantic import BaseModel, Field


class Genre(BaseModel):
    uuid: str = Field(serialization_alias="uuid", validation_alias="id")
    name: str

    class Config:
        populate_by_name = True


class GenreList(BaseModel):
    genres: list[Genre]
