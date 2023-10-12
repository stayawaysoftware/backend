from models.room import Room
from pydantic import BaseModel
from pydantic import Field
from pydantic.config import ConfigDict


class UsersInfo(BaseModel):
    model_config = ConfigDict(title="Users", from_attributes=True)

    min: int
    max: int
    names: list[str]

    @classmethod
    def get_users_info(cls, room: Room):
        users = list(room.users)
        users.sort(key=lambda user: user.id)
        usernames = [user.username for user in users]
        return cls(
            min=room.min_users,
            max=room.max_users,
            names=usernames,
        )


class RoomOut(BaseModel):
    model_config = ConfigDict(title="Room", from_attributes=True)

    id: int
    name: str = Field(max_length=32)
    host_id: int
    in_game: bool = Field(default=False)
    is_private: bool = Field(default=False)
    users: UsersInfo

    @classmethod
    def from_room(cls, room: Room):
        return cls(
            id=room.id,
            name=room.name,
            host_id=room.host_id,
            in_game=room.in_game,
            is_private=room.passw is not None,
            users=UsersInfo.get_users_info(room),
        )
