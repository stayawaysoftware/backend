from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.user import UserOut


def get_users():
    with db_session:
        users = User.select()
    users = [UserOut.from_db(user) for user in users]
    users.sort(key=lambda x: x.id)
    return users


def create_user(username: str):
    with db_session:
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
