from pydantic import BaseModel
from pydantic import Field


class RoomOut(BaseModel):
    id: int
    name: str = Field(max_length=30)
    host_id: int
    min_users: int = Field(4, ge=4, le=12)
    max_users: int = Field(12, ge=4, le=12)

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
