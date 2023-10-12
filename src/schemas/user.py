from models.room import User
from pydantic import BaseModel
from pydantic import ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(title="User", from_attributes=True)

    id: int
    username: str

    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
        )
