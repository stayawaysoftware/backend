from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.room import UserOut

user = APIRouter(tags=["users"])


@user.get(
    "/users",
    response_model=list[UserOut],
    response_description="List the users that were uploaded to the database",
)
def get_users():
    with db_session:
        users = User.select()
        result = [UserOut.from_orm(u) for u in users]
    return result


@user.post(
    "/users",
    response_model=UserOut,
    response_description="Returns the created user",
)
@db_session
def create_user(username: str):

    if User.exists(username=username):
        raise HTTPException(status_code=500, detail="Username already exists")
    user = User(username=username)
    commit()
    return UserOut.from_orm(user)


@user.delete(
    "/users/{id}",
    response_description="Returns 200_OK whit a message when the user is deleted\
        else returns 500 with a error message",
    status_code=status.HTTP_200_OK,
)
@db_session
def delete_user(id: int):
    user = User.get(id=id)
    if user is None:
        raise HTTPException(status_code=500, detail="User does not exist")
    if user.lobby is not None:
        raise HTTPException(status_code=500, detail="User is in a room")
    user.delete()
    commit()
    return {"message": f"User {id} deleted successfully"}
