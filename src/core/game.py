import random

from models.game import Game
from models.game import Player
from models.room import Room
from pony.orm import commit
from pony.orm import db_session


@db_session
def init_game(room_id: int):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (iG)")

    game = Game(id=room_id)
    commit()
    init_players(room_id, game)


@db_session
def init_players(room_id: int, game: Game):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (iP)")

    i = 1
    for user in room.users:
        player = Player(
            name=user.username, id=user.id, round_position=i, game=game
        )
        i += 1

    players = list(game.players)
    player = random.choice(players)
    player.role = "The Thing"
    commit()
