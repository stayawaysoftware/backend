import core.room as rooms
from fastapi import APIRouter
from fastapi import Form
from fastapi import HTTPException
from fastapi import status
from pony.orm import db_session
from schemas.room import RoomOut

from .socket import connection_manager

room = APIRouter(tags=["rooms"])


@room.get(
    "/room/list",
    response_model=list[RoomOut],
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
    response_model=dict[str, int],
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
async def new_room(
    name: str = Form(...),
    password: str = Form(None),
    host_id: int = Form(...),
    min_users: int = Form(4),
    max_users: int = Form(12),
):
    with db_session:
        try:
            room = rooms.create_room(
                name, host_id, min_users, max_users, password
            )
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            if str(error) == "User not found":
                raise HTTPException(status_code=404, detail=str(error))
            else:
                raise HTTPException(status_code=400, detail=str(error))
    # Post to subscribers that a new room has been created
    return {"room_id": room.id}


@room.put(
    "/room/join",
    response_model=dict[str, int],
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
async def join_room(room_id: int = Form(...), user_id: int = Form(...)):
    with db_session:
        try:
            rooms.join_room(room_id, user_id)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
    # Post to subscribers that a user has joined the room
    response = connection_manager.make_room_response(room_id, "join")
    await connection_manager.broadcast(room_id, response)
    return {"room_id": room_id}


@room.put(
    "/room/leave",
    response_description="Returns 200 OK",
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
async def leave_room(room_id: int = Form(...), user_id: int = Form(...)):
    with db_session:
        try:
            room = rooms.leave_room(room_id, user_id)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
    # Post to subscribers that a user has left the room
    if room is not None:
        response = connection_manager.make_room_response(room_id, "leave")
        await connection_manager.broadcast(room_id, response)


@room.put(
    "/room/start",
    response_description="Returns 200 OK",
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
async def play_game(room_id: int = Form(...), host_id: int = Form(...)):
    with db_session:
        try:
            rooms.start_game(room_id, host_id)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
    # Post to subscribers that a game has started
    response = connection_manager.make_room_response(room_id, "start")
    await connection_manager.broadcast(room_id, response)


"""
@room.delete(
    "/room/delete",
    response_description="Returns 204",
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
async def delete_room(room_id: int = Form(...), host_id: int = Form(...)):
    with db_session:
        try:
            rooms.delete_room(room_id, host_id)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
    # Post to subscribers that a room has been deleted
    response = connection_manager.make_room_response(room_id, "delete")
    await connection_manager.broadcast(room_id, response)
"""
