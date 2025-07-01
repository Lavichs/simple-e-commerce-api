import uuid

from pydantic import BaseModel, Field, ConfigDict


class SUserAdd(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    username: str = Field(max_length=100, min_length=1)
    password: str = Field(max_length=100, min_length=10)


class SUser(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: uuid.UUID
    username: str = Field(max_length=100, min_length=1)
    hashed_password: bytes
    is_admin: bool


