import uuid

from pydantic import BaseModel, ConfigDict, Field


class SProductAdd(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    title: str = Field(max_length=100, min_length=1)
    description: str = Field(max_length=1000, min_length=1)
    price: float = Field(gt=0)
    stock_count: int = Field(ge=0)



class SProduct(SProductAdd):
    id: uuid.UUID


