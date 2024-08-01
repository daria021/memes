from pydantic import BaseModel


class FileCreate(BaseModel):
    id: int
    path: str


class FileResponse(BaseModel):
    id: int
    path: str
