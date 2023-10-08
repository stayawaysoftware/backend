import core.user as users
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from pony.orm import db_session
from schemas.room import UserOut

user = APIRouter(tags=["users"])


@user.get(
    "/users",
    response_model=list[UserOut],
    response_description="List the users that were uploaded to the database",
    status_code=status.HTTP_200_OK,
)
def get_users():
    with db_session:
        result = users.get_users()
        result = [UserOut.model_validate(user) for user in result]
    # sort result by id
    result.sort(key=lambda x: x.id)
    return result


@user.post(
    "/users",
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
def create_user(username: str):
    try:
        user = users.create_user(username)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))
    return UserOut.model_validate(user)


@user.delete(
    "/users/{id}",
    response_description="Deletes the user with the given id",
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
def delete_user(id: int):
    try:
        users.delete_user(id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))
