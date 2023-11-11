from models.game import Game
from models.game import Player
from models.room import Room
from pony.orm import commit
from pony.orm import db_session


@db_session
def create_player(
    room_id: int, game: Game, user_id: int, p_round_position: int
):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (cP)")

    # get a user in a room by id
    user = None
    for u in room.users:
        if u.id == user_id:
            user = u
            break
    if user is None:
        raise ValueError("User does not exist")
    player = Player(
        name=user.username,
        id=user.id,
        round_position=p_round_position,
        game=game,
    )
    commit()
    return player
