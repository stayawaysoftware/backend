import core.room as rooms
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from pony.orm import db_session
from schemas.room import RoomOut

room = APIRouter(tags=["rooms"])


@room.get(
    "/rooms",
    response_model=list[RoomOut],
    response_description="List the rooms available in the database",
    status_code=status.HTTP_200_OK,
)
def get_rooms():
    with db_session:
        result = rooms.get_rooms()
        result = [RoomOut.model_validate(room) for room in result]
    return result


@room.get(
    "/rooms/{room_id}",
    response_model=RoomOut,
    response_description="Get a room info by its id",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "Room not found",
        }
    },
)
def get_room(room_id: int):
    with db_session:
        try:
            room = rooms.get_room(room_id)
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
        room = RoomOut.model_validate(room)
    return room


@room.post(
    "/rooms",
    response_model=RoomOut,
    response_description="Returns the created room or an error with details when fail",
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
async def create_room(
    name: str, host_id: int, min_users: int = 4, max_users: int = 12
):
    with db_session:
        try:
            room = rooms.create_room(name, host_id, min_users, max_users)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            if str(error) == "User not found":
                raise HTTPException(status_code=404, detail=str(error))
            else:
                raise HTTPException(status_code=400, detail=str(error))
        room = RoomOut.model_validate(room)
    return room


@room.put(
    "/rooms/{room_id}/join",
    response_model=RoomOut,
    response_description="Returns the joined room or an error with msg when fail",
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
async def join_room(room_id: int, user_id: int):
    with db_session:
        try:
            room = rooms.join_room(room_id, user_id)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
    return room


@room.put(
    "/rooms/{room_id}/leave",
    response_model=RoomOut | None,
    response_description="Returns the left room, 200 with null when the room was deleted\
          or an error with details when fail",
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "User is not in a room, User is not in this room or\
                 game is already in progress",
        },
        404: {
            "description": "User or room not found",
        },
    },
)
async def leave_room(room_id: int, user_id: int):
    with db_session:
        try:
            room = rooms.leave_room(room_id, user_id)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
    if room:
        room = RoomOut.model_validate(room)
    return room


@room.put(
    "/rooms/{room_id}/start",
    response_model=RoomOut,
    response_description="Returns the started room or an error with details when fail",
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "User is not in a room, User is not the host of this Room,\
            not enough Users in this Room or Games is alredy in progress."
        },
        404: {
            "description": "User or room not found",
        },
    },
)
async def play_game(room_id: int, host_id: int):
    with db_session:
        try:
            room = rooms.start_game(room_id, host_id)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
    return room


@room.delete(
    "/rooms/{room_id}",
    response_description="Returns an error with details when fail",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        403: {
            "description": "User is not the host of this room",
        },
        404: {
            "description": "Room not found",
        },
    },
)
async def delete_room(room_id: int, host_id: int):
    with db_session:
        try:
            rooms.delete_room(room_id, host_id)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
