import core.user as users
from fastapi import APIRouter
from fastapi import status
from pony.orm import db_session
from schemas.user import UserId
from schemas.user import Username
from schemas.user import UserOut

user = APIRouter(tags=["users"])


@user.get(  # ONLY FOR DEBUG
    "/user/list",
    response_model=list[UserOut],
    response_description="List the users that were uploaded to the database",
    status_code=status.HTTP_200_OK,
)
def get_users():
    with db_session:
        result = users.get_users()
    return result


@user.post(
    "/user/new",
    response_model=UserOut,
    response_description="Returns the created user",
    status_code=status.HTTP_201_CREATED,
    responses={
        403: {
            "description": "User already exists",
        }
    },
)
@db_session
def create_user(username: Username):
    user = users.create_user(username.username)
    return UserOut.from_db(user)


@user.delete(
    "/user/delete",
    response_description="Returns 204 No Content",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "description": "User not found",
        },
        403: {
            "description": "User is in a room",
        },
    },
)
@db_session
def delete_user(id: UserId):
    users.delete_user(id.id)
