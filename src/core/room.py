import hashlib
from typing import Optional

import core.game as game
from models.room import Room
from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.room import RoomListItem
from models.game import Game
from models.game import Player


def hashing(pwd):
    hash_object = hashlib.md5(bytes(str(pwd), encoding="utf-8"))
    hex_dig = hash_object.hexdigest()
    return hex_dig


@db_session
def get_rooms():
    rooms = Room.select()
    result = [RoomListItem.from_db(room) for room in rooms]
    return result


@db_session
def create_room(
    name: str,
    host_id: int,
    min_users: int = 4,
    max_users: int = 12,
    pwd: Optional[str] = None,
):
    if not User.exists(id=host_id):
        raise ValueError("User not found")
    if User[host_id].room is not None:
        raise PermissionError("User is already in a room")
    if min_users < 4 or min_users > 12:
        raise ValueError("Minimum users invalid value")
    if max_users < 4 or max_users > 12:
        raise ValueError("Maximum users invalid value")
    if min_users > max_users:
        raise ValueError("Minimum users must be less than maximum users")
    if pwd is not None:
        pwd = hashing(pwd)
    with db_session:
        room = Room(
            name=name,
            pwd=pwd,
            host_id=host_id,
            in_game=False,
            min_users=min_users,
            max_users=max_users,
        )

        User[host_id].room = room
        commit()
        room_id = room.id

    return room_id


@db_session
def join_room(room_id: int, user_id: int):
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if not User.exists(id=user_id):
        raise ValueError("User not found")
    user = User.get(id=user_id)
    room = Room.get(id=room_id)
    if len(room.users) >= room.max_users:
        raise PermissionError("Room is full")
    if user.room is not None:
        raise PermissionError("User is already in a room")
    if Room.get(id=room_id).in_game:
        raise PermissionError("Game is already in progress")
    room = Room.get(id=room_id)
    user.room = room
    commit()


@db_session
def leave_room(room_id: int, user_id: int):
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if not User.exists(id=user_id):
        raise ValueError("User not found")
    user = User.get(id=user_id)
    room = Room.get(id=room_id)
    if user.room is None:
        raise PermissionError("User is not in a room")
    if user.room.id != room_id:
        raise PermissionError("User is not in this room")
    if room.in_game:
        raise PermissionError("Game is already in progress")
    if len(room.users) == 0 or room.host_id == user_id:
        delete_room(room_id, user_id)
        commit()
        return None
    User[user_id].room = None
    commit()
    return room_id


@db_session
def start_game(room_id: int, host_id: int):
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if not User.exists(id=host_id):
        raise ValueError("User not found")
    user = User.get(id=host_id)
    if user.room is None:
        raise PermissionError("User is not in a room")
    if user.room.id != room_id:
        raise PermissionError("User is not in this room")
    if user.room.host_id != host_id:
        raise PermissionError("User is not the host")
    if user.room.in_game:
        raise PermissionError("Game is already in progress")
    if len(user.room.users) < user.room.min_users:
        raise PermissionError("Not enough users to start the game")
    room = Room.get(id=room_id)
    game.init_game(room_id)
    room.in_game = True
    commit()


@db_session
def delete_room(room_id: int, host_id: int):
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if not User.exists(id=host_id):
        raise ValueError("User not found")
    room = Room.get(id=room_id)
    user = User.get(id=host_id)
    if room.host_id != host_id:
        raise PermissionError("User is not the host")
    if room.in_game:
        raise PermissionError("Game is already in progress")
    if user.room is None:
        raise PermissionError("User is not in a room")
    if user.room.id != room_id:
        raise PermissionError("User is not in this room")
    for user in room.users:
        user.room = None
    room.delete()
    commit()


@db_session
def delete_game(game_id: int):
    room = Room.get(id=game_id)
    for user in room.users:
        player = Player.get(id=user.id)
        player.delete()
        commit()
        room_id = leave_room(game_id, user.id)
    game = Game.get(id=room_id)
    if game is not None:
        game.delete()
    commit()