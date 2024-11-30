

from pydantic import BaseModel

class AddItem(BaseModel):
    id: int
    classID: int
    SystemInTime: str

class DeleteItem(BaseModel):
    id: int
    classID: int
    SystemOutTime: str

class NextIDResponse(BaseModel):
    nextID: int
