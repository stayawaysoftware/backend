from pydantic import BaseModel
from pydantic import Field


class RoomOut(BaseModel):
    id: int
    name: str = Field(max_length=30)
    host_id: int
    in_game: bool
    usernames: list[str]

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
