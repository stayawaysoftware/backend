from enum import Enum

from models.game import Game
from models.room import Room
from models.room import User
from pydantic import BaseModel
from pydantic import Field
from pydantic.config import ConfigDict
from schemas import validators
from schemas.game import GameInfo

from .room import RoomId
from .room import RoomInfo
from .room import UsersInfo

# ======================= Auxiliar Enums =======================


class RoomEventTypes(Enum):
    INFO = "info"
    LEAVE = "leave"
    START = "start"
    JOIN = "join"
    DELETE = "delete"

    @classmethod
    def has_type(cls, key):
        return key in cls.__members__


class GameEventTypes(str, Enum):
    START = "start"
    PLAY = "play"
    GAME_STATUS = "game_status"
    DEFENSE = "defense"
    EXCHANGE = "exchange"
    EXCHANGE_DEFENSE = "exchange_defense"
    FINISHED = "finished"
    DISCARD = "discard"
    END = "end"

    @classmethod
    def has_type(cls, key):
        return key in cls.__members__


# ======================= Input Schemas =======================


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
    def create(cls, message: str, sender: int):
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

    @classmethod
    def create(cls, type: GameEventTypes, room_id: RoomId):
        game = Game.get(id=room_id)
        match type:
            case "game_info":
                return {
                    "type": type,
                    "game": GameInfo.from_db(game),
                }
