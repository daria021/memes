from pydantic import BaseModel, ConfigDict


class MemeCreate(BaseModel):
    name: str
    description: str


class MemeUpdate(BaseModel):
    name: str
    description: str


class MemeResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class MemeFilter(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


