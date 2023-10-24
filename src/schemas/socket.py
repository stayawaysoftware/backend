from enum import Enum

import schemas.validators as validators
from models.game import Game
from models.room import Room
from models.room import User
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from pydantic.config import ConfigDict
from schemas.game import GameInfo

from .room import RoomId
from .room import RoomInfo
from .room import UsersInfo

# ======================= Auxiliar Enums =======================


class RoomEventTypes(Enum):
    info = "info"
    leave = "leave"
    start = "start"
    join = "join"
    delete = "delete"

    @classmethod
    def has_type(cls, key):
        return key in cls.__members__


class GameEventTypes(str, Enum):
    start = "start"
    play = "play"
    game_status = "game_status"
    defense = "defense"
    exchange = "exchange"
    exchange_defense = "exchange_defense"
    end = "end"

    @classmethod
    def has_type(cls, key):
        return key in cls.__members__


# ======================= Input Schemas =======================


class EventInRoom(BaseModel):
    model_config = ConfigDict(title="EventInRoom")
    type: RoomEventTypes = Field(...)


class EventInGame(BaseModel):
    pass


class ChatMessage(BaseModel):
    type: str = Field("message")
    message: str = Field(...)
    sender: int = Field(...)
    room_id: int = Field(...)

    @classmethod
    def validate(cls, sender, room_id):
        user_id = sender  # Rename to reuse validator
        sender = validators.SocketValidators.validate_user_exists(user_id)
        values = {"room_id": room_id}  # Rename to reuse validator
        sender, values = validators.SocketValidators.validate_user_in_room(
            user_id, values
        )

    @classmethod
    def create(cls, message: str, sender: int, room_id: int):
        sendername = User.get(id=sender).username
        return {
            "type": "message",
            "message": message,
            "sender": sendername,
        }


# ======================= Output Schemas =======================


class ErrorMessage(BaseModel):
    model_config = ConfigDict(title="ErrorMessage")
    # type cant be setted, always is error
    type: str = Field("error")
    message: str = Field(...)

    @classmethod
    def format(cls, message: str):
        if "Assertion failed, " in message:
            message = message.split("Assertion failed, ")[1]
            message = message.split(" [")[0]
        return message

    @classmethod
    def create(cls, message: str):
        message = cls.format(message)
        return {
            "type": "error",
            "description": message,
        }


class RoomMessage(BaseModel):
    model_config = ConfigDict(title="RoomMessage")

    type: RoomEventTypes = Field(...)

    @validator("type", pre=True, allow_reuse=True)
    def validate_type(cls, type):
        assert RoomEventTypes.has_type(type), "Invalid type"
        return type

    @classmethod
    def create(cls, type: RoomEventTypes, room_id: RoomId):
        room = Room.get(id=room_id)
        match type:
            case "info":
                return {
                    "type": type,
                    "room": RoomInfo.from_db(room),
                }
            case "delete":
                return {
                    "type": type,
                }
            case _:
                return {
                    "type": type,
                    "room": {
                        "users": UsersInfo.get_users_info(room),
                    },
                }


class GameMessage(BaseModel):
    model_config = ConfigDict(title="GameMessage")

    type: GameEventTypes = Field(...)

    @validator("type", pre=True, allow_reuse=True)
    def validate_type(cls, type):
        assert GameEventTypes.has_type(type), "Invalid type"
        return type

    @classmethod
    def create(cls, type: GameEventTypes, room_id: RoomId):
        game = Game.get(id=room_id)
        match type:
            case "game_info":
                return {
                    "type": type,
                    "game": GameInfo.from_db(game),
                }
