from fastapi import APIRouter
from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.room import UserInDB
from fastapi import HTTPException

user = APIRouter(tags=["users"])


@user.get(
    "/users",
    response_model=list[UserInDB],
    response_description="List the users that were uploaded to the database",
)
def get_users():
    with db_session:
        users = User.select()
        result = [UserInDB.from_orm(u) for u in users]
    return result


@user.post(
    "/users",
    response_model=UserInDB,
    response_description="Returns the created user",
)
def create_user(username: str):
    with db_session:
        if User.exists(username=username):
            raise HTTPException(status_code=500, detail="Username already exists")
        user = User(username=username)
        user.lobby = None
        commit()
    return user
