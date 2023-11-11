from models.room import User
from pony.orm import commit
from pony.orm import db_session


def create_user(username: str):
    with db_session:
        if User.exists(username=username):
            raise PermissionError("User already exists")
        user = User(username=username)
        commit()
    return user


def delete_user(id: int):
    with db_session:
        user = User.get(id=id)
        if user is None:
            raise ValueError("User not found")
        if user.room is not None:
            raise PermissionError("User is in a room")
        user.delete()
        commit()
