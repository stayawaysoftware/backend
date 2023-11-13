import random
from typing import Optional

import core.game_logic.game_utility as gu
from core.connections import ConnectionManager
from core.effect_handler import effect_handler
from core.game_logic.card import relate_card_with_player
from core.game_logic.card import unrelate_card_with_player
from core.game_logic.card_creation import card_defense
from core.player import create_player
from fastapi import HTTPException
from core.game_logic.game_effects import get_defense_cards
from models.game import Card
from models.game import Game
from models.game import Player
from models.room import Room
from pony.orm import commit
from pony.orm import db_session
from schemas.card import CardOut
from schemas.player import PlayerOut


connection_manager = ConnectionManager()


@db_session
def init_players(room_id: int, game: Game):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (iP)")

    # To get random order of players
    user_list = list(room.users)
    random.shuffle(user_list)

    # To get random order of positions
    round_position = list(range(1, len(user_list) + 1))
    random.shuffle(round_position)

    # Create players and deal cards

    index = 0
    while index < len(user_list):
        player = create_player(
            room_id, game, user_list[index].id, round_position[index]
        )
        gu.get_initial_player_hand(room_id, player.id)
        index += 1

    # Set the thing
    for player in game.players:
        if player.hand.filter(idtype=1).count() > 0:
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

        effect = effect_handler(
            game_id, card_idtype, current_player_id, target_player_id
        )
        game.current_phase = "Discard"
        commit()
        gu.discard(
            id_game=game_id,
            idtype_card=card_idtype,
            id_player=current_player.id,
        )
    except ValueError as e:
        print("ERROR:", str(e))

    return effect


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
        "played_card": card.model_dump(by_alias=True, exclude_unset=True),
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
            player = PlayerOut.to_json(player)

        card = Card.get(id=played_card)
        card = CardOut.from_card(card)
        defended_by = card_defense[card.idtype]
        res = {
            "type": "try_defense",
            "target_player": card_target,
            "played_card": card.model_dump(by_alias=True, exclude_unset=True),
            "defended_by": defended_by,
        }
    return res


@db_session
def check_winners(game_id: int):
    game = Game.get(id=game_id)
    players = list(game.players)
    alive_players = list(filter(lambda p: p.alive, players))
    infected_players = list(
        filter(lambda p: p.role == "Infected", alive_players)
    )
    human_alive_players = list(
        filter(lambda p: p.role == "Human", alive_players)
    )
    the_thing_player = list(filter(lambda p: p.role == "The Thing", players))[
        0
    ]
    if (infected_players == len(alive_players) - 1) or len(
        human_alive_players
    ) == 0:
        game.winners = "The Thing"
        commit()
        game.status = "Finished"
        commit()
    elif not the_thing_player.alive:
        game.winners = "Humans"
        commit()
        game.status = "Finished"
        commit()


@db_session
def not_defended_card(
    last_card_played_id: int,
    game_id: int,
    attacker_id: int,
    defense_player_id: int,
):
    at = Card.get(id=last_card_played_id)
    attack_card = CardOut.from_card(at)
    try:


        effect = play_card(game_id, at.idtype, attacker_id, defense_player_id)
        response = {
            "type": "defense",
            "type": "defense",
            "played_defense": 0,
            "target_player": defense_player_id,
            "last_played_card": attack_card.model_dump(
                by_alias=True, exclude_unset=True
            ),
        }
    except ValueError as e:
        print("ERROR:", str(e))

    return response, effect



@db_session
def defended_card(
    game_id: int,
    attacker_id: int,
    defense_player_id: int,
    last_card_played_id: int,
    defense_card_id: int,
):
    try:
        at = Card.get(id=last_card_played_id)
        de = Card.get(id=defense_card_id)
        attack_card = CardOut.from_card(at)
        defense_card = CardOut.from_card(de)
        game = Game.get(id=game_id)
    except ValueError as e:
        print("ERROR:", str(e))


    game.current_phase = "Discard"
    commit()
    gu.discard(game_id, at.idtype, attacker_id)
    gu.discard(game_id, de.idtype, defense_player_id)
    game.current_phase = "Draw"
    commit()
    draw_card(game_id, defense_player_id)
    response = {
        "type": "defense",
        "played_defense": defense_card.model_dump(
            by_alias=True, exclude_unset=True
        ),
        "target_player": defense_player_id,
        "last_played_card": attack_card.model_dump(
            by_alias=True, exclude_unset=True
        ),
    }
    return response



@db_session
def handle_defense(
    game_id: int,
    card_type_id: int,
    attacker_id: int,
    last_card_played_id: int,
    defense_player_id: int,
):
    try:
        response = None
        game = Game.get(id=game_id)
        effect = None
    except ValueError as e:
        print("ERROR:", str(e))

    if card_type_id == 0:
        try:
            response, effect = not_defended_card(
                last_card_played_id, game_id, attacker_id, defense_player_id
            )
            
        except ValueError as e:
            print("ERROR:", str(e))
    else:
        attack_card = Card.get(id=last_card_played_id)
        defense_card = Card.get(id=card_type_id)
        if defense_card.idtype in get_defense_cards(attack_card.idtype):
            try:
                response = defended_card(game_id, attacker_id, defense_player_id, last_card_played_id, card_type_id)
                effect = effect_handler(game_id, defense_card.idtype, defense_player_id, attacker_id, last_card_played_id)
            except ValueError as e:
                print("ERROR:", str(e)) 
        else:
            raise ValueError("Card cant be defended with that card")
    try:
        check_winners(game_id)
        game.current_phase = "Exchange"
        commit()
    except ValueError as e:
        print("ERROR:", str(e))


    return response, effect

@db_session
def draw_card(game_id: int, player_id: int):
    id3 = gu.draw(game_id, player_id)
    card = Card.get(id=id3)
    card = CardOut.from_card(card)

    draw_response = {
        "type": "draw",
        "new_card": card.model_dump(by_alias=True, exclude_unset=True),
    }

    return draw_response


@db_session
def handle_exchange(
    exchange_requester: int, chosen_card: int, target_player: int
):
    card = Card.get(id=chosen_card)
    card = CardOut.from_card(card)
    exchange_defense = card_defense[32]
    exchange_response = {
        "type": "exchange_defense",
        "defended_by": exchange_defense,
        "last_chosen_card": card.model_dump(by_alias=True, exclude_unset=True),
        "target_player": target_player,
        "exchange_requester": exchange_requester,
    }
    return exchange_response

@db_session
def exchange_defended(
    game_id : int,
    current_player_id: int,
    defense_card_id: int,
):
    game = Game.get(id=game_id)
    game.current_phase = "Discard"
    defense_card = Card.get(id=defense_card_id)
    commit()
    gu.discard(game_id, defense_card.idtype, current_player_id)
    game.current_phase = "Draw"
    commit()
    gu.draw(game_id, current_player_id)

@db_session
def exchange_not_defended(
    game_id : int,
    current_player_id: int,
    last_chosen_card: int,
    exchange_requester: int,
    chosen_card: int,
):
    effect = effect_handler(game_id ,32,current_player_id,exchange_requester,last_chosen_card,chosen_card)
    return effect

@db_session
def handle_exchange_defense(
    game_id: int,
    current_player_id: int,
    exchange_requester: int,
    last_chosen_card: int,
    chosen_card: int,
    is_defense: bool,
):
    game = Game.get(id=game_id)
    effect = None
    if is_defense:
        defense_card = Card.get(id=chosen_card)
        if defense_card.idtype in get_defense_cards(32):
            try:
                defense_card = Card.get(id=chosen_card)
                exchange_defended(game_id, current_player_id, chosen_card)
                effect = effect_handler(game_id, defense_card.idtype, current_player_id, exchange_requester, last_chosen_card)
            except ValueError as e:
                print("ERROR:", str(e))
        else:
            raise ValueError("Exchange cant be defended with that card")
    else:
        try:
            effect = exchange_not_defended(game_id, current_player_id, last_chosen_card, exchange_requester, chosen_card)
        except ValueError as e:
            print("ERROR:", str(e))
    calculate_next_turn(game_id)
    players = list(game.players)
    next_player =list(filter(lambda p: p.round_position == game.current_position, players))[0]
    game.current_phase = "Draw"
    commit()
    try:
        gu.draw(game_id, next_player.id)
    except ValueError as e:
            print("ERROR:", str(e))

    return effect

@db_session
def sospecha_effect(target_id: int, user_id: int):
    # TODO: Mirar una carta aleatoria de un jugador adyacente
    target_hand = list(Player.get(id=target_id).hand)
    random_card = CardOut.from_card(random.choice(target_hand))
    response = show_one_card_effect(target_id, user_id, random_card.id)
    return response

@db_session
def show_one_card_effect(target_id: int, user_id: int, target_chosen_card_id: int):
    target = Player.get(id=target_id)
    target_card = CardOut.from_card(Card.get(id=target_chosen_card_id))
    response = {
        "type": "show_card",
        "player_name" : target.name,
        "target" : [user_id],
        "cards": [target_card.dict(by_alias=True, exclude_unset=True)]
    }
    return response

@db_session
def show_hand_effect(game_id: int, target_id: int):
    target_player = PlayerOut.to_json(Player.get(id=target_id))
    target_hand = target_player["hand"]
    players = Game.get(id=game_id).players
    target = []
    for p in players:
        target.append(p.id)
    response = {
        "type": "show_card",
        "player_name": target_player["name"],
        "target": target,
        "cards": target_hand,
    }
    return response

@db_session
def vigila_tus_espaldas_effect(game_id: int):
    game = Game.get(id=game_id)
    game.round_left_direction = not game.round_left_direction
    commit()

@db_session
def position_change_effect(target_id: int, user_id: int):
    target = Player.get(id=target_id)
    user = Player.get(id=user_id)
    user_position = user.round_position
    user.round_position = target.round_position
    target.round_position = user_position
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

def flamethower_effect(target_id: int):
    target_player = Player.get(id=target_id)
    target_player.alive = False
    commit()
