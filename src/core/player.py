import random
from pony.orm import db_session, commit
from models.game import Deck
from models.game import Game
from models.game import Player
from models.room import Room
import core.game_utility as gu


@db_session
def init_players(room_id: int, game: Game, deck: Deck):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (iP)")

    i = 1
    for user in room.users:
        player = Player(
            name=user.username, id=user.id, round_position=i, game=game
        )
        if i == 1:  # First player
            gu.draw_card_from_deck(room_id, player)
        for j in range(4):
            gu.draw_card_from_deck(room_id, player)

        i += 1

    players = list(game.players)
    player = random.choice(players)
    player.role = "The Thing"
    commit()