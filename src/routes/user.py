from fastapi import APIRouter
from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.room import UserInDB

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
    response_model=int,
    response_description="Returns the id of the created user",
)
async def create_user(username: str):
    with db_session:
        user = User(username=username)
        commit()
        print("CREATED:\t ", user.id, " - ", user.username)
    return user.id
