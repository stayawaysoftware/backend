import core.room as rooms
from fastapi import HTTPException
from models.room import Room
from models.room import User
from pydantic import validator


class EndpointValidators:
    """A class with validators that raise HTTPExceptions
    Only used in new room, join room, create user and delete user
    methods which are an endpoint in the API
    """

    @classmethod
    @validator("max_users", pre=True, allow_reuse=True)
    def validate_max_users(cls, max_users):
        if max_users > 12 or max_users < 4:
            raise HTTPException(
                status_code=400, detail="Maximum users invalid value"
            )
        return max_users

    @classmethod
    @validator("min_users", pre=True, allow_reuse=True)
    def validate_min_users(cls, min_users):
        if min_users > 12 or min_users < 4:
            raise HTTPException(
                status_code=400, detail="Minimum users invalid value"
            )
        return min_users

    @classmethod
    @validator("max_users", "min_users", allow_reuse=True)
    def validate_max_min_users(cls, max_users, values):
        max_users = max_users
        min_users = values["min_users"]

        if max_users < min_users:
            raise HTTPException(
                status_code=400,
                detail="Maximum users must be greater than minimum users",
            )

        return max_users, values

    @classmethod
    @validator("user_id", pre=True, allow_reuse=True)
    def validate_user_exists(cls, user_id):
        if not User.get(id=user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return user_id

    @classmethod
    @validator("room_id", pre=True, allow_reuse=True)
    def validate_room_exists(cls, room_id):
        if not Room.get(id=room_id):
            raise HTTPException(status_code=404, detail="Room not found")
        return room_id

    @classmethod
    @validator("user_id", pre=True, allow_reuse=True)
    def validate_user_not_in_room(cls, user_id):
        if User.exists(id=user_id):
            if User.get(id=user_id).room is not None:
                raise HTTPException(
                    status_code=403, detail="User is already in a room"
                )
        return user_id

    @classmethod
    @validator("room_id", pre=True, allow_reuse=True)
    def validate_room_not_full(cls, room_id):
        if Room.get(id=room_id):
            room = Room.get(id=room_id)
            if len(room.users) >= room.max_users:
                raise HTTPException(status_code=403, detail="Room is full")
        return room_id

    @classmethod
    @validator("room_id", pre=True, allow_reuse=True)
    def validate_room_not_in_game(cls, room_id):
        if Room.get(id=room_id):
            if Room.get(id=room_id).in_game:
                raise HTTPException(
                    status_code=403, detail="Game is already in progress"
                )
        return room_id

    @classmethod
    @validator("username", pre=True, allow_reuse=True)
    def validate_username_not_exists(cls, username):
        if User.get(username=username):
            raise HTTPException(status_code=403, detail="User already exists")
        return username

    @classmethod
    @validator("password", pre=True, allow_reuse=True)
    def validate_password(cls, password, values):
        room_id = values["room_id"]
        if Room.get(id=room_id):
            room = Room.get(id=room_id)
            if room.pwd is not None:
                if rooms.hashing(password) != room.pwd:
                    raise HTTPException(
                        status_code=403, detail="Wrong password"
                    )
        return password


class SocketValidators:
    """A class with validators that create error messages
    Used in all other methods which have a socket connection
    """

    @classmethod
    @validator("user_id", pre=True, allow_reuse=True)
    def validate_user_exists(cls, user_id):
        assert User.get(id=user_id), "User not found"
        return user_id

    @classmethod
    @validator("room_id", pre=True, allow_reuse=True)
    def validate_room_exists(cls, room_id):
        assert Room.get(id=room_id), "Room not found"
        return room_id

    @classmethod
    @validator("user_id", "room_id", pre=True, allow_reuse=True)
    def validate_user_in_room(cls, user_id, values):
        room_id = values["room_id"]
        user = User.get(id=user_id)
        assert user.room is not None, "User is not in a room"
        assert user.room.id == room_id, "User is not in this room"
        return user_id, values

    @classmethod
    @validator("user_id", "room_id", pre=True, allow_reuse=True)
    def validate_user_is_host(cls, user_id, values):
        room_id = values["room_id"]
        assert Room.get(id=room_id).host_id == user_id, "User is not the host"
        return user_id, values

    @classmethod
    @validator("room_id", pre=True, allow_reuse=True)
    def validate_room_not_in_game(cls, room_id):
        assert not Room.get(id=room_id).in_game, "Game is already in progress"
        return room_id

    @classmethod
    @validator("room_id", pre=True, allow_reuse=True)
    def validate_room_have_almost_min_users(cls, room_id):
        room = Room.get(id=room_id)
        assert (
            len(room.users) >= room.min_users
        ), "Room does not have enough users"
        return room_id
