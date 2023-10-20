import random
from typing import Optional

import core.game_utility as gu
import core.room as Iroom
from core.connections import ConnectionManager
from core.player import create_player
from core.player import dealing_cards
from fastapi import HTTPException
from models.game import Game
from models.game import Player
from models.room import Room
from pony.orm import commit
from pony.orm import db_session
from schemas.game import GameStatus
from schemas.player import PlayerOut

connection_manager = ConnectionManager()


@db_session
def init_players(room_id: int, game: Game):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (iP)")

    i = 1
    for user in room.users:
        player = create_player(room_id, game, user.id, i)
        dealing_cards(room_id, player, i)
        i += 1

    players = list(game.players)
    player = random.choice(players)
    player.role = "The Thing"
    commit()


@db_session
def init_game(room_id: int):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (iG)")
    deck = gu.initialize_decks(
        id_game=room_id, quantity_players=len(room.users)
    )
    game = Game(id=room_id, deck=deck)
    commit()
    init_players(room_id, game)


@db_session
def init_game_status(game_id: int):
    players = Game.get(id=game_id).players
    player_list = [PlayerOut.from_player(p) for p in players]
    the_thing_player = Player.select(lambda p: p.role == "The Thing").first()
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
    effect = gu.play(
        id_game=game_id,
        id_player=current_player_id,
        idtype_card=card_idtype,
        target=target_player_id,
        first_play=False
    )
    game.current_phase = "Discard"
    commit()
    gu.discard(
        id_game=game_id, idtype_card=card_idtype, id_player=current_player.id
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
    target_player_id: Optional[int] = None,
):
    play_card(
        game_id=game.id,
        card_idtype=card_idtype,
        current_player_id=current_player_id,
        target_player_id=target_player_id,
    )
    players = Game.get(id=game.id).players
    player_list = [PlayerOut.from_player(p) for p in players]
    calculate_next_turn(game_id=game.id)
    next_player = Player.select(
        lambda p: p.round_position == game.current_position
    ).first()
    gu.draw(id_game=game.id, id_player=next_player.id)
    game.current_phase = "Draw"
    commit()
    the_thing_player = Player.select(lambda p: p.role == "The Thing").first()
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
        next_player = Player.select(
            lambda p: p.round_position == next_player_position
        ).first()
        if next_player.alive:
            break
    game.current_position = next_player_position
    print("Next player is: " + str(next_player_position))
    commit()


@db_session
def delete_game(game_id: int):
    game = Game.get(id=game_id)
    players = Game.get(id=game_id).players
    if players is None:
        raise HTTPException(status_code=404, detail="Players not found")
    for p in players:
        p.delete()
    game.delete()
    commit()
    room = Room.get(id=game.id)
    Iroom.delete_room(room.id, room.host_id)


def handle_play(
    card_type_id: int,
    target_player_id: int,
):
    response = {
        "type": "play",
        "played_card": card_type_id,
        "card_target": target_player_id,
    }
    return response


@db_session
def try_defense(played_card: int, card_target: int):
    with db_session:
        player = Player.get(id=card_target)
        player = PlayerOut.json(player)
        res = {
            "type": "try_defense",
            "target_player": card_target,
            "played_card": played_card,
            "defended_by": player["hand"]
        }
    return res


@db_session
def handle_defense(
    game_id: int,
    card_type_id: int,
    defense_player_id: int,
    last_card_played_id: int,
    attacker_id: int
):
    print("IF interno del handle")
    if card_type_id is None:
        play_card(game_id, last_card_played_id, attacker_id, defense_player_id)
    else:
        game = Game.get(id=game_id)
        try:
            print("ENTRA AL ELSE")
            game.current_phase = "Discard"
            commit()
            id = gu.discard(game_id, last_card_played_id, attacker_id)
            print(id, "PRIMER ID")
            id = gu.discard(game_id, card_type_id, defense_player_id)
            print(id, "SEGUNDO ID")
            game.current_phase="Draw"
            commit()
            id = gu.draw(game_id, defense_player_id)
            print("SALE DEL ELSE")
        except ValueError as e:
            print("ERROR:", str(e))  # Imprime el mensaje de error de la excepción

    

    current_turn = Game.get(id=game_id).current_position

    response = {
        "type": "new_turn",
         "current_turn":current_turn
    }

    return response
