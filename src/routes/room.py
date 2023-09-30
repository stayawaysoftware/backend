"""Room routes"""
from fastapi import APIRouter
from fastapi import HTTPException
from models.room import Room
from models.room import User
from pony.orm import commit
from pony.orm import db_session
from schemas.room import RoomOut

# Create a router instance
room_router = APIRouter(tags=["rooms"])


# Connections
@room_router.get(
    "/rooms",
    response_model=list[RoomOut],
    response_description="List the rooms that were uploaded to the database",
)
def get_rooms():
    """Get all the rooms in the database"""
    with db_session:
        rooms = Room.select()
        result = [RoomOut.from_orm(u) for u in rooms]
    return result


@room_router.get(
    "/rooms/{room_id}/users",
    response_model=list[str],
    response_description="List the usernames that are in the room",
)
def get_users_in_room(room_id: int):
    """Get all the users in a room"""
    with db_session:
        if not Room.exists(id=room_id):
            raise HTTPException(status_code=500, detail="Room does not exist")
        users = Room.get(id=room_id).users
        # Get the usernames of the users in the room
        result = [u.username for u in users]
    return result


@room_router.post(
    "/rooms",
    response_model=RoomOut,
    response_description="Returns the created room",
)
async def create_room(
    name: str, host_id: int, min_users: int = 4, max_users: int = 12
):
    """Create a room"""
    with db_session:
        if not User.exists(id=host_id):
            raise HTTPException(status_code=500, detail="User does not exist")
        if User.get(id=host_id).lobby is not None:
            raise HTTPException(
                status_code=500, detail="User is already in a room"
            )
        if min_users < 4 or min_users > 12 or min_users > max_users:
            raise HTTPException(
                status_code=500, detail="Minimum users invalid value"
            )
        if max_users < 4 or max_users > 12 or max_users < min_users:
            raise HTTPException(
                status_code=500, detail="Maximum users invalid value"
            )

        room = Room(
            name=name,
            host_id=host_id,
            min_users=min_users,
            max_users=max_users,
        )
        User[host_id].lobby = room
        commit()
    return room
