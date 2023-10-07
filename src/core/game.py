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
from schemas.game import GameStatus
from schemas.player import PlayerOut
from core.game_utility import draw_card_from_deck


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
        if i == 1:  # First player
            gu.draw_card_from_deck(room_id, player)
        for j in range(4):
            gu.draw_card_from_deck(room_id, player)

        i += 1

    players = list(game.players)
    player = random.choice(players)
    player.role = "The Thing"
    commit()


@db_session
def init_game_status(game_id: int):
        players = Game.get(id=game_id).players
        player_list = [PlayerOut.from_player(p) for p in players]
        the_thing_player = Player.get(role="The Thing")
        the_thing_player_status = the_thing_player.alive
        game_status = GameStatus(
            players=player_list,
            alive_players=len(list(filter(lambda p: p.alive, players))),
            the_thing_is_alive=the_thing_player_status,
            turn_phase=Game.get(id=game_id).current_phase,
            current_turn=Game.get(id=game_id).current_position,
            lastPlayedCard=None,
        )
        return game_status

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
def turn_game_status(
                    game: Game,
                    card_idtype: int, 
                    current_player_id: int,
                    target_player_id: Optional[int] = None):
        play_card(
            game_id=game.id,
            card_idtype=card_idtype,
            current_player_id=current_player_id,
            target_player_id=target_player_id,
        )
        players = Game.get(id=game.id).players
        player_list = [PlayerOut.from_player(p) for p in players]
        calculate_next_turn(game_id=game.id)
        next_player = Player.get(round_position=game.current_position)
        draw_card_from_deck(id_game=game.id, player=next_player)
        game.current_phase = "Draw"
        commit()
        the_thing_player = Player.get(role="The Thing")
        the_thing_player_status = the_thing_player.alive

        game_status = GameStatus(
            players=player_list,
            alive_players=len(list(filter(lambda p: p.alive, players))),
            the_thing_is_alive=the_thing_player_status,
            turn_phase=Game.get(id=game.id).current_phase,
            current_turn=Game.get(id=game.id).current_position,
            lastPlayedCard=card_idtype,
        )
        return game_status



@db_session
def calculate_next_turn(game_id: int):
    game = Game.get(id=game_id)
    players = list(game.players)
    current_player_position = game.current_position
    # select as next player the next player alive in the round direction
    next_player_position = current_player_position
    while True:
        next_player_position += 1
        if next_player_position > len(players):
            next_player_position = 1
        next_player = Player.get(round_position=next_player_position)
        if next_player.alive:
            break
    game.current_position = next_player_position
    print("Next player is: " + str(next_player_position))
    commit()
