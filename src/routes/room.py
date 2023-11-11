import core.room as rooms
from fastapi import APIRouter
from fastapi import status
from pony.orm import db_session
from schemas.room import RoomCreateForm
from schemas.room import RoomId
from schemas.room import RoomJoinForm
from schemas.room import RoomListItem
from schemas.socket import RoomMessage

from .socket import connection_manager

room = APIRouter(tags=["rooms"])


@room.get(
    "/room/list",
    response_model=list[RoomListItem],
    response_description="Returns 200 OK with a list of rooms\
          available in the database",
    status_code=status.HTTP_200_OK,
)
def get_rooms():
    with db_session:
        result = rooms.get_rooms()
    return result


@room.post(
    "/room/new",
    response_model=RoomId,
    name="Create a new room",
    response_description="Returns 201 Created with the room id",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Minimum or maximum users invalid value",
        },
        403: {
            "description": "User is already in a room",
        },
    },
)
async def new_room(room_form_data: RoomCreateForm):
    with db_session:
        room_id = rooms.create_room(
            room_form_data.name,
            room_form_data.host_id,
            room_form_data.min_users,
            room_form_data.max_users,
            room_form_data.password,
        )
    return RoomId.create(room_id)


@room.put(
    "/room/join",
    response_model=RoomId,
    name="Join a room",
    response_description="Returns 200 OK with the room id",
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "Room is full, user is already in a room or\
                 game is already in progress",
        },
        404: {
            "description": "User or room not found",
        },
    },
)
async def join_room(join_form_data: RoomJoinForm):
    with db_session:
        rooms.join_room(join_form_data.room_id, join_form_data.user_id)
    # Post to subscribers that a user has joined the room
    response = RoomMessage.create("join", join_form_data.room_id)
    await connection_manager.broadcast(join_form_data.room_id, response)
    return RoomId.create(join_form_data.room_id)
