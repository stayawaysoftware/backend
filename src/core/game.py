import random
from typing import Optional

import core.game_utility as gu
import core.room as Iroom
from core.connections import ConnectionManager
from core.card_creation import card_defense
from core.player import create_player
from core.player import dealing_cards
from core.effect_handler import effect_handler
from core.card import relate_card_with_player
from core.card import unrelate_card_with_player
from fastapi import HTTPException
from models.game import Game
from models.game import Player
from models.room import Room
from models.game import Card
from pony.orm import commit
from pony.orm import db_session
from schemas.game import GameStatus
from schemas.player import PlayerOut
from schemas.card import CardOut


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
    """
    for p in players:
        for c in p.hand:
            if c.idtype == 2:
                p.role = "The Thing"
                break
    """
    
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
    try:
        game = Game.get(id=game_id)
        game.current_phase = "Play"
        commit()
        current_player = Player.get(id=current_player_id)
        if target_player_id == 0:
            target_player_id = None
        print("Llego al handler")
        
        effect = effect_handler(game_id,card_idtype,current_player_id,target_player_id)
        print("effect")
        print("Sale del handler")
        game.current_phase = "Discard"
        commit()
        gu.discard(
            id_game=game_id, idtype_card=card_idtype, id_player=current_player.id
        )
    except ValueError as e:
        print("ERROR:", str(e))
    
    return effect


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
        if not game.round_left_direction:
            next_player_position += 1
            if next_player_position > len(players):
                next_player_position = 1
        else:
            next_player_position -= 1
            if next_player_position < 1:
                next_player_position = len(players)
        next_player = None  # Inicializa a None para evitar errores si no se encuentra el siguiente jugador
        for player in players:
            if player.round_position == next_player_position:
                next_player = player
                break
        if next_player is not None and next_player.alive:
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


def handle_play(
    card_id: int,
    target_player_id: int,
):
    card = Card.get(id=card_id)
    card = CardOut.from_card(card)
    response = {
        "type": "play",
        "played_card": card.dict(by_alias=True, exclude_unset=True),
        "card_target": target_player_id,
    }
    return response


@db_session
def try_defense(played_card: int, card_target: int):
    with db_session:
        if card_target == 0:
            print("No se puede defender")
        else:
            player = Player.get(id=card_target)
            player = PlayerOut.json(player)

        card = Card.get(id=played_card)
        card = CardOut.from_card(card)
        defended_by = card_defense[card.idtype]
        res = {
            "type": "try_defense",
            "target_player": card_target,
            "played_card": card.dict(by_alias=True, exclude_unset=True),
            "defended_by": defended_by
        }
    return res

@db_session
def check_winners(game_id:int):
    game = Game.get(id=game_id)
    players = list(game.players)
    infected_players = list(filter(lambda p: p.role == "Infected", players))
    human_players = list(filter(lambda p: p.role == "Human", players))
    the_thing_player = Player.select(lambda p: p.role == "The Thing").first()
    if (infected_players == len(players) - 1) or len(human_players) == 0:
        game.winners = "The Thing"
        commit()
        game.status = "Finished"
    elif not the_thing_player.alive:
        game.winners = "Humans"
        commit()
        game.status = "Finished"
        commit()

@db_session
def handle_defense(
    game_id: int,
    card_type_id: int,
    attacker_id: int,
    last_card_played_id: int,
    defense_player_id: int
):
    
    draw_response = None
    response = None
    defense_card = Card.get(id=card_type_id)
    defense_card = CardOut.from_card(defense_card)
    attack_card = Card.get(id=last_card_played_id)
    attack_card = CardOut.from_card(attack_card)
    game = Game.get(id=game_id)
    effect = None
    if last_card_played_id == 11:
        effect = seduccion_effect(game_id)
        response = {
                "type" : "defense",
                "played_defense": 0,
                "target_player": defense_player_id,
                "last_played_card": attack_card.dict(by_alias=True, exclude_unset=True)
            }
    else:
        if card_type_id == 0:
            try:
                at = Card.get(id=last_card_played_id)
                effect = play_card(game_id, at.idtype, attacker_id, defense_player_id)
            except ValueError as e:
                print("ERROR:", str(e))
            response = {
                "type" : "defense",
                "played_defense": 0,
                "target_player": defense_player_id,
                "last_played_card": attack_card.dict(by_alias=True, exclude_unset=True)
            }
        else:
            at = Card.get(id=last_card_played_id)
            de = Card.get(id=card_type_id)
            try:
                game.current_phase = "Discard"
                commit()
                id1 = gu.discard(game_id, at.idtype, attacker_id)
                id2 = gu.discard(game_id, de.idtype, defense_player_id)
                game.current_phase="Draw"
                commit()
                draw_response = draw_card(game_id, defense_player_id)
                response = {
                    "type" : "defense",
                    "played_defense": defense_card.dict(by_alias=True, exclude_unset=True),
                    "target_player": defense_player_id,
                    "last_played_card": attack_card.dict(by_alias=True, exclude_unset=True)
                }
            except ValueError as e:
                print("ERROR:", str(e))  # Imprime el mensaje de error de la excepción

        check_winners(game_id)
        print ("DRAW RESPONSE")
        game.current_phase = "Exchange"
        commit()
        
    return response, effect

@db_session
def draw_card(game_id: int, player_id: int):
    id3 = gu.draw(game_id, player_id)
    card = Card.get(id=id3)
    card = CardOut.from_card(card)


    draw_response = {
                    "type":"draw",
                    "new_card": card.dict(by_alias=True, exclude_unset=True)
                  }
    
    return draw_response

@db_session
def handle_exchange(
    exchange_requester:int,
    chosen_card: int,
    target_player: int
):
    card = Card.get(id=chosen_card)
    card = CardOut.from_card(card)
    exchange_defense = card_defense[32]
    exchange_response = {
        "type": "exchange_defense",
        "defended_by": exchange_defense,
        "last_chosen_card": card.dict(by_alias=True, exclude_unset=True),
        "target_player": target_player,
        "exchange_requester" : exchange_requester
    }
    return exchange_response

@db_session
def handle_exchange_defense(
    game_id : int,
    current_player_id: int,
    exchange_requester:int,
    last_chosen_card: int,
    chosen_card: int,
    is_defense: bool
):
    game = Game.get(id=game_id)
    if is_defense:
        try:
            print("Pre-disc")
            game.current_phase = "Discard"
            commit()
            print("Aft-disc")
            gu.discard(game_id, last_chosen_card, current_player_id)
            print("Aft-disc")
            game.current_phase = "Draw"
            commit()
            gu.draw(game_id, current_player_id)
            print("Aft-draw")
        except ValueError as e:
            print("ERROR:", str(e))
    else:
        try:
            print("Pre-EffectHandler")
            print("Effect handler args: ", game_id ,32,current_player_id,exchange_requester,last_chosen_card,chosen_card)
            effect = effect_handler(game_id ,32,current_player_id,exchange_requester,last_chosen_card,chosen_card)
            print("After-EffectHandler")
        except ValueError as e:
           print("ERROR:",str(e))
    calculate_next_turn(game_id)
    next_player = Player.select(
        lambda p: p.round_position == game.current_position
    ).first()
    game.current_phase = "Draw"
    commit()
    try:
         gu.draw(game_id, next_player.id)
    except ValueError as e:
            print("ERROR:", str(e))
    print("Exchange finalizado")

@db_session
def analisis_effect(game_id: int, adyacent_id: int):
    #TODO: Revisar que sea adyacente
    adyacent_player  = Player.get(id=adyacent_id)
    adyacent_player_json = PlayerOut.json(adyacent_player)
    cards = adyacent_player_json["hand"]
    players = Game.get(id=game_id).players
    target = []
    for p in players:
        target.append(p.id)
    response = {
        "type": "show_card",
        "player_name": adyacent_player.name,
        "target": target,
        "cards": cards
    }
    return response

@db_session
def vigila_tus_espaldas_effect(game_id: int):
    game = Game.get(id=game_id)
    game.round_left_direction = not game.round_left_direction
    commit()

@db_session
def exchange_effect(target_id: int, user_id: int, target_chosen_card:int, user_chosen_card:int):
    print("Entra en exchange effect")
    target = Player.get(id=target_id)
    user = Player.get(id=user_id)
    target_card = Card.get(id=target_chosen_card)
    user_card = Card.get(id=user_chosen_card)

    unrelate_card_with_player(target_card.id, target.id)
    unrelate_card_with_player(user_card.id, user.id)
    relate_card_with_player(target_card.id, user.id)
    relate_card_with_player(user_card.id, target.id)

    user_is_the_thing = (user_card.idtype == 2) and (user.role == "The Thing")
    target_is_the_thing = (target_card.idtype == 2) and (target.role == "The Thing")

    if user_is_the_thing:
        target.role = "Infected"
        commit()
    
    if target_is_the_thing:
        user.role = "Infected"
        commit()

@db_session
def cambio_de_lugar_effect(target_id: int, user_id: int):
    #TODO: implementar que si hay obstaculos o cuarentena no se puede usar y verificar que sea adyacente
    target = Player.get(id=target_id)
    user = Player.get(id=user_id)
    user_position = user.round_position
    user.round_position = target.round_position
    target.round_position = user_position
    commit()

@db_session
def mas_vale_que_corras_effect(target_id: int, user_id: int):
    target = Player.get(id=target_id)
    user = Player.get(id=user_id)
    user_position = user.round_position
    user.round_position = target.round_position
    target.round_position = user_position
    commit()

@db_session
def seduccion_effect(game_id: int):
    game = Game.get(id=game_id)
    game.current_phase = "Exchange"
    commit()

@db_session
def sospecha_effect(target_id: int, user_id: int):
    #TODO: Mirar una carta aleatoria de un jugador adyacente
    target = Player.get(id=target_id)
    target_hand = list(target.hand)
    random_card = random.choice(target_hand)
    random_card = CardOut.from_card(random_card)
    response = {
        "type": "show_card",
        "player_name": target.name,
        "target":[user_id],
        "cards": [random_card.dict(by_alias=True, exclude_unset=True)]
    }
    return response

@db_session
def whisky_effect(game_id,user_id: int):
    player = Player.get(id=user_id)
    player_json = PlayerOut.json(player)
    cards = player_json["hand"]
    #Add every player from game_id to targe tarray
    players = Game.get(id=game_id).players
    target = []
    for p in players:
        target.append(p.id)
    response = {
        "type": "show_card",
        "player_name": player.name,
        "target": target,
        "cards": cards
    }
    return response

def flamethower_effect(target_id: int):
    target_player = Player.get(id=target_id)
    target_player.alive = False
    commit()