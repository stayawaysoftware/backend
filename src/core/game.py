import random
from typing import Optional

import core.game_utility as gu
from core.effects import do_effect
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
        if i == 1: #First player
            gu.draw_card_from_deck(room_id, player)
        for j in range(4):
            gu.draw_card_from_deck(room_id, player)

        i += 1

    players = list(game.players)
    player = random.choice(players)
    player.role = "The Thing"
    commit()


@db_session
def play_card(
    game_id: int,
    card_idtype: int,
    current_player_id: int,
    target_player_id: Optional[int] = None,
):
    game = Game.get(id=game_id)
    game.current_phase = "Play"
    commit()
    current_player = Player.get(id=current_player_id)
    effect = do_effect(
        id_game=game_id, id_card_type=card_idtype, target=target_player_id
    )
    gu.discard_card(
        id_game=game_id, id_card_type=card_idtype, player=current_player
    )
    if str(effect.get_action()) == "Kill":
        target_player = Player.get(id=target_player_id)
        target_player.alive = False
        commit()


@db_session
def calculate_next_turn(game_id: int):
    game = Game.get(id=game_id)
    players = list(game.players)
    current_player_position = game.current_position
    # select as next player the next player alive in the round direction
    next_player = None
    next_player_position = current_player_position + 1 % len(players)
    while next_player is None:
        if players[next_player_position].alive:
            next_player = players[next_player_position]
        else:
            next_player_position = next_player_position + 1 % len(players)
    game.current_position = next_player_position
    commit()
