from enum import Enum

from models.room import Room
from models.room import User
from pydantic import BaseModel
from pydantic import Field
from pydantic.config import ConfigDict

from .room import RoomId
from .room import RoomOut


# ======================= Auxiliar Enums =======================


class RoomEventTypes(Enum):
    leave = "leave"
    start = "start"
    join = "join"
    delete = "delete"

    @classmethod
    def has_type(cls, key):
        return key in cls.__members__


class GameEventTypes(str, Enum):
    start = "start"
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


class ChatMessageIn(BaseModel):
    type: str = Field("message")
    message: str = Field(...)


# ======================= Output Schemas =======================


class ErrorMessage(BaseModel):
    model_config = ConfigDict(title="ErrorMessage")
    # type cant be setted, always is error
    type: str = Field("error")
    message: str = Field(...)

    @classmethod
    def create(cls, message: str):
        # if message contains "Assertion failed," cut it
        if "Assertion failed, " in message:
            message = message.split("Assertion failed, ")[1]
        return {
            "type": "error",
            "description": message,
        }


class RoomMessage(BaseModel):
    model_config = ConfigDict(title="RoomMessage")

    type: RoomEventTypes = Field(...)
    room: RoomOut = Field(...)

    @classmethod
    def create(cls, type: RoomEventTypes, room_id: RoomId):
        return {"type": type, "room": RoomOut.from_db(Room.get(id=room_id))}


class ChatMessageOut(BaseModel):
    model_config = ConfigDict(title="ChatMessage")
    type: str = Field("message")
    message: str = Field(...)
    sender: str = Field(...)

    @classmethod
    def create(cls, message: str, user_id: int):
        sender = User.get(id=user_id).username
        return {"type": "message", "message": message, "sender": sender}
