from models.room import Room
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from pydantic.config import ConfigDict

from .validators import ValidatorsHttpRaise


# ======================= Input Schemas =======================


class RoomCreateForm(BaseModel):
    name: str = Field(max_length=32)
    password: str = Field(max_length=32, nullable=True)
    host_id: int = Field(gt=0)
    min_users: int
    max_users: int

    @validator("max_users", allow_reuse=True)
    def validate_max_min_users(cls, max_users, values):
        max_users = max_users
        min_users = values["min_users"]
        max_users = ValidatorsHttpRaise.validate_max_users(max_users)
        min_users = ValidatorsHttpRaise.validate_min_users(min_users)
        max_users, values = ValidatorsHttpRaise.validate_max_min_users(
            max_users, values
        )
        return max_users

    @validator("host_id", pre=True, allow_reuse=True)
    def validate_host_id(cls, host_id):
        user_id = host_id  # Rename to reuse validator
        user_id = ValidatorsHttpRaise.validate_user_exists(user_id)
        user_id = ValidatorsHttpRaise.validate_user_not_in_room(user_id)
        return user_id


class RoomJoinForm(BaseModel):
    room_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    password: str = Field(max_length=32, nullable=True)

    @validator("room_id", pre=True, allow_reuse=True)
    def validate_room_id(cls, room_id):
        room_id = ValidatorsHttpRaise.validate_room_exists(room_id)
        room_id = ValidatorsHttpRaise.validate_room_not_full(room_id)
        room_id = ValidatorsHttpRaise.validate_room_not_in_game(room_id)
        return room_id

    @validator("user_id", pre=True, allow_reuse=True)
    def validate_user_id(cls, user_id):
        user_id = ValidatorsHttpRaise.validate_user_exists(user_id)
        user_id = ValidatorsHttpRaise.validate_user_not_in_room(user_id)
        return user_id


# ======================= Output Schemas =======================


class RoomId(BaseModel):
    id: int = Field(gt=0)

    @classmethod
    def create(cls, id):
        return cls(
            id=id,
        )


class UsersInfo(BaseModel):
    model_config = ConfigDict(title="Users", from_attributes=True)

    min: int = Field(gt=3, lt=13)
    max: int = Field(gt=3, lt=13)
    names: list[str]

    @classmethod
    def get_users_info(cls, room: Room):
        users = list(room.users)
        users.sort(key=lambda user: user.id)
        usernames = [user.username for user in users]
        return {
            "min": room.min_users,
            "max": room.max_users,
            "names": usernames,
        }


class RoomOut(BaseModel):
    model_config = ConfigDict(title="Room", from_attributes=True)

    id: int
    name: str = Field(max_length=32)
    host_id: int = Field(gt=0)
    in_game: bool = Field(default=False)
    is_private: bool = Field(default=False)
    users: UsersInfo

    @classmethod
    def from_db(cls, room: Room):
        return {
            "id": room.id,
            "name": room.name,
            "host_id": room.host_id,
            "in_game": room.in_game,
            "is_private": room.passw is not None,
            "users": UsersInfo.get_users_info(room),
        }
