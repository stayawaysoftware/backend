import core.game as cg
from models.room import Room
from models.room import User
from pony.orm import commit
from pony.orm import db_session


@db_session
def update_usernames(room: Room):
    dict_users = {u.username: u.id for u in room.users}
    room.usernames = [u.username for u in room.users]
    # sort usernames by your id
    room.usernames.sort(key=lambda x: dict_users[x])


@db_session
def get_rooms():
    rooms = Room.select()
    result = []
    for room in rooms:
        room.usernames = [u.username for u in room.users]
        result.append(room)
    # sort result by id
    result.sort(key=lambda x: x.id)
    return result


@db_session
def get_room(id: int):
    room = Room.get(id=id)
    if room is None:
        raise ValueError("Room not found")
    update_usernames(room)
    return room


@db_session
def create_room(
    name: str, host_id: int, min_users: int = 4, max_users: int = 12
):
    with db_session:

        if not User.exists(id=host_id):
            raise ValueError("User not found")
        if User.get(id=host_id).room is not None:
            raise PermissionError("User is already in a room")
        if min_users < 4 or min_users > 12 or min_users > max_users:
            raise ValueError("Minimum users invalid value")
        if max_users < 4 or max_users > 12 or max_users < min_users:
            raise ValueError("Maximum users invalid value")

        room = Room(
            name=name,
            host_id=host_id,
            in_game=False,
            min_users=min_users,
            max_users=max_users,
        )

        User[host_id].room = room
        update_usernames(room)
        commit()
    return room


@db_session
def join_room(room_id: int, user_id: int):
    if not User.exists(id=user_id):
        raise ValueError("User not found")
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if User.get(id=user_id).room is not None:
        raise PermissionError("User is already in a room")
    room = Room.get(id=room_id)
    if len(room.users) >= room.max_users:
        raise PermissionError("Room is full")
    if room.in_game:
        raise PermissionError("Game is already in progress")
    User[user_id].room = room
    update_usernames(room)
    commit()
    return room


@db_session
def leave_room(room_id: int, user_id: int):
    if not User.exists(id=user_id):
        raise ValueError("User not found")
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if User.get(id=user_id).room is None:
        raise PermissionError("User is not in a room")
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is already in progress")
    if not User[user_id] in room.users:
        raise PermissionError("User is not in this room")
    if len(room.users) == 0 or room.host_id == user_id:
        delete_room(room_id, user_id)
        User[user_id].room = None
        return None
    User[user_id].room = None
    update_usernames(room)
    commit()
    return room


@db_session
def start_game(room_id: int, host_id: int):
    if not User.exists(id=host_id):
        raise ValueError("User not found")
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if User.get(id=host_id).room is None:
        raise PermissionError("User is not in a room")
    room = Room.get(id=room_id)
    if room.id != User[host_id].room.id:
        raise PermissionError("User is not in this room")
    if room.in_game:
        raise PermissionError("Game is already in progress")
    if room.host_id != host_id:
        raise PermissionError("User is not the host of this room")
    if len(room.users) < room.min_users:
        raise PermissionError("Not enough users in this room")
    cg.init_game(room_id)
    room.in_game = True
    update_usernames(room)
    commit()
    return room


@db_session
def delete_room(room_id: int, host_id: int):
    if not User.exists(id=host_id):
        raise ValueError("User not found")
    if not Room.exists(id=room_id):
        raise ValueError("Room not found")
    if User.get(id=host_id).room is None:
        raise PermissionError("User is not in a room")
    room = Room.get(id=room_id)
    if room.id != User[host_id].room.id:
        raise PermissionError("User is not in this room")
    if room.in_game:
        raise PermissionError("Game is already in progress")
    if room.host_id != host_id:
        raise PermissionError("User is not the host of this room")
    for user in room.users:
        user.room = None
    room.delete()
    commit()
