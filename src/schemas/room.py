from typing import Optional

from pydantic import BaseModel


class UserInDB(BaseModel):
    id: int
    username: str
    id_lobby: Optional[str]

    class Config:
        from_attributes = True
