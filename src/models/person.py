from pydantic import BaseModel, Field


class Person(BaseModel):
    id: str = Field(serialization_alias="uuid")
    name: str = Field(serialization_alias="full_name")
