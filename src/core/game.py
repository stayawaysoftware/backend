import random

import core.game_utility as gu
from models.game import Deck
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
    deck = gu.first_deck_creation(room_id, len(list(room.users)))
    game = Game(id=room_id, deck=deck)
    commit()
    init_players(room_id, game, deck)


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
        for j in range(4):
            gu.draw_card_from_deck(room_id, player)
        
        print(player.hand)
        i += 1

    players = list(game.players)
    player = random.choice(players)
    player.role = "The Thing"
    commit()
