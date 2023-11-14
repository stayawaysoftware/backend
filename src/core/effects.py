import random
import core.game_logic.game_utility as gu

from typing import Optional
from pony.orm import db_session
from pony.orm import commit
from models.game import Player
from models.game import Card
from models.game import Game
from schemas.socket import GameMessage
from schemas.card import CardOut
from core.game_logic.card import relate_card_with_player
from core.game_logic.card import unrelate_card_with_player



@db_session
def sospecha_effect(game_id: int,target_id: int, user_id: int):
    target_hand = list(Player.get(id=target_id).hand)
    random_card = CardOut.from_card(random.choice(target_hand))
    response = show_one_card_effect(game_id, user_id, random_card.id)
    return response

@db_session
def show_one_card_effect(game_id, player_id: int, target_chosen_card_id: int, target_id: Optional[int] = None):
    response = GameMessage.create(type="show_card",
                                    room_id=game_id, 
                                    quarantined=None, 
                                    card_id=target_chosen_card_id,
                                    player_id=player_id,
                                    target_id=target_id,
                                   )
    return response

@db_session
def show_hand_effect(game_id: int, player_id: int, target_id: Optional[int] = None):
    response = GameMessage.create(type="show_hand",
                                  room_id=game_id,
                                  quarantined=None,
                                  card_id=None,
                                  player_id=player_id,
                                  target_id=target_id,)
    return response


@db_session
def vigila_tus_espaldas_effect(game_id: int):
    game = Game.get(id=game_id)
    game.round_left_direction = not game.round_left_direction
    commit()


@db_session
def position_change_effect(game_id: int, target_id: int, user_id: int):
    (
        Player[target_id].round_position,
        Player[user_id].round_position,
    ) = (
        Player[user_id].round_position,
        Player[target_id].round_position,
    )

    Game[game_id].current_position = Player[user_id].round_position
    commit()

@db_session
def exchange_effect(
    target_id: int,
    user_id: int,
    target_chosen_card: int,
    user_chosen_card: int,
):
    target = Player.get(id=target_id)
    user = Player.get(id=user_id)
    target_card = Card.get(id=target_chosen_card)
    user_card = Card.get(id=user_chosen_card)

    unrelate_card_with_player(target_card.id, target.id)
    unrelate_card_with_player(user_card.id, user.id)
    relate_card_with_player(target_card.id, user.id)
    relate_card_with_player(user_card.id, target.id)

    user_is_the_thing = (user_card.idtype == 2) and (user.role == "The Thing")
    target_is_the_thing = (target_card.idtype == 2) and (
        target.role == "The Thing"
    )

    if user_is_the_thing:
        target.role = "Infected"
        commit()

    if target_is_the_thing:
        user.role = "Infected"
        commit()

@db_session
def seduccion_effect(game_id: int):
    game = Game.get(id=game_id)
    game.current_phase = "Exchange"
    commit()

@db_session
def flamethower_effect(target_id: int):
    target_player = Player.get(id=target_id)
    target_player.alive = False
    commit()

@db_session
def locked_door_effect(game_id: int, target_id: int):
    game = Game.get(id=game_id)
    position = Player.get(id=target_id).round_position - 1
    game.locked_doors[position] = 1
    commit()

@db_session
def axe_effect(game_id: int, target_id: int):
    game = Game.get(id=game_id)
    position = Player.get(id=target_id).round_position - 1
    game.locked_doors[position] = 0
    commit()

@db_session
def quarantine_effect(target_id: int):
    player = Player.get(id=target_id)
    player.quarantine = 2
    commit()

@db_session
def test_cuatro_effect(game_id: int):
    game = Game.get(id=game_id)
    for p in list(game.players):
        for i in list(p.hand):
            if i.idtype == 18:
                game.current_phase = "Discard"
                commit()
                gu.discard(game_id, 18, p.id)
                game.current_phase = "Draw"
                gu.draw(game_id, p.id)
        commit()

@db_session

@db_session
def cuerdas_podridas_effect(game_id: int):
    game = Game.get(id=game_id)
    for p in list(game.players):
        for i in list(p.hand):
            if i.idtype == 18:
                game.current_phase = "Discard"
                commit()
                gu.discard(game_id, 19, p.id)
                game.current_phase = "Draw"
                gu.draw(game_id, p.id)
    commit()

@db_session
def olvidadizo_effect(game_id: int, user_id: int):
    game = Game.get(id=game_id)
    player = Player.get(id=user_id)
    for i in list(player.hand):
        j = 0
        if i.idtype != 1 and j<3:
            game.current_phase = "Discard"
            commit()
            gu.discard(game_id, i.idtype, user_id)
            j+=1
        for i in range(3):
            game.current_phase = "Draw"
            gu.draw_no_panic(game_id, user_id)
    commit()

@db_session
def cita_a_ciegas_effect(game_id: int, user_id: int):
    game = Game.get(id=game_id)
    game.current_phase = "Discard"
    commit()
    user_hand = list(Player.get(id=user_id).hand)
    random_card = CardOut.from_card(random.choice(user_hand))
    gu.discard(game_id, random_card.idtype, user_id)
    game.current_phase = "Draw"
    gu.draw_no_panic(game_id, user_id)
    commit()

