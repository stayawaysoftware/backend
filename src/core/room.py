import hashlib
from typing import Optional

import core.game as game
from models.room import Room
from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.room import RoomListItem


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
    room = Room.get(id=room_id)
    User[user_id].room = room
    commit()


@db_session
def leave_room(room_id: int, user_id: int):
    room = Room.get(id=room_id)
    if len(room.users) == 0 or room.host_id == user_id:
        delete_room(room_id, user_id)
        User[user_id].room = None
        return None
    User[user_id].room = None
    commit()
    room = RoomListItem.from_db(room)
    return room


@db_session
def start_game(room_id: int, host_id: int):
    room = Room.get(id=room_id)
    game.init_game(room_id)
    room.in_game = True
    commit()


@db_session
def delete_room(room_id: int, host_id: int):
    room = Room.get(id=room_id)
    for user in room.users:
        user.room = None
    room.delete()
    commit()
