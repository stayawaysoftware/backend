from fastapi import APIRouter
from fastapi import HTTPException
from models.room import Room
from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.room import RoomOut

room = APIRouter(tags=["rooms"])


@room.get(
    "/rooms",
    response_model=list[RoomOut],
    response_description="List the rooms available in the database",
)
def get_rooms():
    with db_session:
        rooms = Room.select()
        result = []
        for room in rooms:
            room.usernames = [u.username for u in room.users]
            result.append(room)
    return result


@room.get(
    "/rooms/{room_id}",
    response_model=RoomOut,
    response_description="Get a room info by its id",
)
def get_room_info(room_id: int):
    with db_session:
        if not Room.exists(id=room_id):
            raise HTTPException(status_code=500, detail="Room does not exist")
        room = Room.get(id=room_id)
        room.usernames = [u.username for u in room.users]
    return room


@room.post(
    "/rooms",
    response_model=RoomOut,
    response_description="Returns the created room or an error with details when fail",
)
async def create_room(
    name: str, host_id: int, min_users: int = 4, max_users: int = 12
):
    with db_session:
        if not User.exists(id=host_id):
            raise HTTPException(status_code=500, detail="User does not exist")
        if User.get(id=host_id).lobby is not None:
            raise HTTPException(
                status_code=500, detail="User is already in a room"
            )
        if min_users < 4 or min_users > 12 or min_users > max_users:
            raise HTTPException(
                status_code=500, detail="Minimum users invalid value"
            )
        if max_users < 4 or max_users > 12 or max_users < min_users:
            raise HTTPException(
                status_code=500, detail="Maximum users invalid value"
            )

        room = Room(
            name=name,
            host_id=host_id,
            in_game=False,
            min_users=min_users,
            max_users=max_users,
        )
        User[host_id].lobby = room
        room.usernames = [u.username for u in room.users]
        commit()
    return room


@room.post(
    "/rooms/{room_id}/join",
    response_model=RoomOut,
    response_description="Returns the joined room or an error with details when fail",
)
async def join_room(room_id: int, user_id: int):
    with db_session:
        if not User.exists(id=user_id):
            raise HTTPException(status_code=500, detail="User does not exist")
        if not Room.exists(id=room_id):
            raise HTTPException(status_code=500, detail="Room does not exist")
        if User.get(id=user_id).lobby is not None:
            raise HTTPException(
                status_code=500, detail="User is already in a room"
            )
        room = Room.get(id=room_id)
        if len(room.users) >= room.max_users:
            raise HTTPException(status_code=500, detail="Room is full")
        if room.in_game:
            raise HTTPException(
                status_code=500, detail="Game is already in progress"
            )
        User[user_id].lobby = room
        room.usernames = [u.username for u in room.users]
        commit()
    return room


@room.post(
    "/rooms/{room_id}/leave",
    response_model=RoomOut | dict,
    response_description="Returns the left room or an error with details when fail",
)
async def leave_room(room_id: int, user_id: int):
    with db_session:
        if not User.exists(id=user_id):
            raise HTTPException(status_code=500, detail="User does not exist")
        if not Room.exists(id=room_id):
            raise HTTPException(status_code=500, detail="Room does not exist")
        if User.get(id=user_id).lobby is None:
            raise HTTPException(
                status_code=500, detail="User is not in a room"
            )
        room = Room.get(id=room_id)
        if room.in_game:
            raise HTTPException(
                status_code=500, detail="Game is already in progress"
            )
        if not User[user_id] in room.users:
            raise HTTPException(
                status_code=500, detail="User is not in this room"
            )
        if len(room.users) == 1:
            room.delete()
            commit()
            return {"detail": f"Room {room_id} deleted successfully"}
        User[user_id].lobby = None
        room.usernames = [u.username for u in room.users]
        commit()
    return room


@room.delete(
    "/rooms/{room_id}",
    response_description="Returns message whit information about the deleted\
        room or an error with details when fail",
    status_code=200,
)
async def delete_room(room_id: int):
    with db_session:
        if not Room.exists(id=room_id):
            raise HTTPException(status_code=500, detail="Room does not exist")
        room = Room.get(id=room_id)
        if room.in_game:
            raise HTTPException(
                status_code=500, detail="Game is already in progress"
            )
        for user in room.users:
            user.lobby = None
        room.delete()
        commit()
    return {"detail": f"Room {room_id} deleted successfully"}


@room.post(
    "/rooms/{room_id}/start",
    response_model=RoomOut,
    response_description="Returns the started room or an error with details when fail",
)
async def play_game(room_id: int, host_id: int):
    with db_session:
        if not User.exists(id=host_id):
            raise HTTPException(status_code=500, detail="User does not exist")
        if not Room.exists(id=room_id):
            raise HTTPException(status_code=500, detail="Room does not exist")
        if User.get(id=host_id).lobby is None:
            raise HTTPException(
                status_code=500, detail="User is not in a room"
            )
        room = Room.get(id=room_id)
        if room.in_game:
            raise HTTPException(
                status_code=500, detail="Game is already in progress"
            )
        if room.host_id != host_id:
            raise HTTPException(
                status_code=500, detail="User is not the host of this room"
            )
        if len(room.users) < room.min_users:
            raise HTTPException(
                status_code=500, detail="Not enough users in this room"
            )
        room.in_game = True
        room.usernames = [u.username for u in room.users]
        # TODO: Create a game instance and save in the database of games
        # TODO: Create a player instance for each user in the room
        commit()
    return room
