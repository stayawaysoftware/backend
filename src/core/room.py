from typing import Optional

import core.game as game
from models.room import Room
from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.room import RoomOut


@db_session
def get_rooms():
    rooms = Room.select()
    result = [RoomOut.from_db(room) for room in rooms]
    return result


@db_session
def create_room(
    name: str,
    host_id: int,
    min_users: int = 4,
    max_users: int = 12,
    password: Optional[str] = None,
):
    with db_session:
        room = Room(
            name=name,
            passw=password,
            host_id=host_id,
            in_game=False,
            min_users=min_users,
            max_users=max_users,
        )

        User[host_id].room = room
        commit()
        room = RoomOut.from_db(room)

    return room


@db_session
def join_room(room_id: int, user_id: int, password: Optional[str] = None):
    room = Room.get(id=room_id)
    User[user_id].room = room
    room = RoomOut.from_db(room)
    commit()
    return room


@db_session
def leave_room(room_id: int, user_id: int):
    room = Room.get(id=room_id)
    """
    if not User.exists(id=user_id):
        raise ValueError("User not found")
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if User.get(id=user_id).room is None:
        raise PermissionError("User is not in a room")

    if room.in_game:
        raise PermissionError("Game is already in progress")
    if not User[user_id] in room.users:
        raise PermissionError("User is not in this room")
    """
    if len(room.users) == 0 or room.host_id == user_id:
        delete_room(room_id, user_id)
        User[user_id].room = None
        return None
    User[user_id].room = None
    commit()
    room = RoomOut.from_db(room)
    return room


@db_session
def start_game(room_id: int, host_id: int):
    """
    if not User.exists(id=host_id):
        raise ValueError("User not found")
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if User.get(id=host_id).room is None:
        raise PermissionError("User is not in a room")

    if room.id != User[host_id].room.id:
        raise PermissionError("User is not in this room")
    if room.in_game:
        raise PermissionError("Game is already in progress")
    if room.host_id != host_id:
        raise PermissionError("User is not the host of this room")
    if len(room.users) < room.min_users:
        raise PermissionError("Not enough users in this room")
    """
    room = Room.get(id=room_id)
    game.init_game(room_id)
    room.in_game = True
    commit()


@db_session
def delete_room(room_id: int, host_id: int):
    """
    if not User.exists(id=host_id):
        raise ValueError("User not found")
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if User.get(id=host_id).room is None:
        raise PermissionError("User is not in a room")
    """
    room = Room.get(id=room_id)
    """
    if room.id != User[host_id].room.id:
        raise PermissionError("User is not in this room")
    if room.in_game:
        raise PermissionError("Game is already in progress")
    if room.host_id != host_id:
        raise PermissionError("User is not the host of this room")
    for user in room.users:
        user.room = None
    """
    room.delete()
    commit()
