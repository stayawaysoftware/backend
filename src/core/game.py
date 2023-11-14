import random
from typing import Optional

import core.game_logic.game_utility as gu
from core.connections import ConnectionManager
from core.game_logic.game_effects import play
from core.game_logic.game_utility import draw_no_panic
from core.game_logic.game_utility import get_defense_cards
from core.player import create_player
from models.game import Card
from models.game import Game
from models.game import Player
from models.room import Room
from pony.orm import commit
from pony.orm import db_session
from schemas.card import CardOut
from schemas.socket import GameMessage


connection_manager = ConnectionManager()


@db_session
def get_card_idtype(card_id: int):
    card = Card.get(id=card_id)
    return card.idtype


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
            break

    # The first player to game must to have one extra card (role position 1)
    for player in game.players:
        if player.round_position == game.current_position:
            gu.draw(room_id, player.id)
            break

    commit()


@db_session
def init_game(room_id: int):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (iG)")
    deck = gu.initialize_decks(
        id_game=room_id, quantity_players=len(room.users)
    )
    locked_doors = [0 for i in range(len(room.users))]
    game = Game(id=room_id, deck=deck, locked_doors=locked_doors)
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

        effect = play(
            id_game=game_id,
            attack_player_id=current_player_id,
            defense_player_id=target_player_id,
            idtype_attack_card=card_idtype,
            idtype_defense_card=0,
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


def handle_play(
    game_id: int,
    card_id: int,
    target_player_id: int,
):
    response = GameMessage.create(
        "play", room_id=game_id, card_id=card_id, target_id=target_player_id
    )
    return response


@db_session
def try_defense(game_id: int, played_card: int, card_target: int):
    with db_session:
        res = GameMessage.create(
            type="try_defense",
            room_id=game_id,
            target_id=card_target,
            card_id=played_card,
        )
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
def handle_not_target(
    game_id: int,
    card_id: int,
    current_player_id: int,
):
    try:
        response = None
        effect = None
        game = Game.get(id=game_id)
        card = Card.get(id=card_id)
        card_idtype = card.idtype

        effect = play(
            id_game=game_id,
            attack_player_id=current_player_id,
            defense_player_id=current_player_id,
            idtype_attack_card=card_idtype,
            idtype_defense_card=0,
        )

        game.current_phase = "Discard"
        commit()
        gu.discard(game_id, card_idtype, current_player_id)
        game.current_phase = "Exchange"
        commit()
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
    draw_no_panic(game_id, defense_player_id)
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

                effect = play(
                    id_game=game_id,
                    attack_player_id=attacker_id,
                    defense_player_id=defense_player_id,
                    idtype_attack_card=attack_card.idtype,
                    idtype_defense_card=defense_card.idtype,
                )

                response = defended_card(
                    game_id,
                    attacker_id,
                    defense_player_id,
                    last_card_played_id,
                    card_type_id,
                )

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
    card_type = card.type
    card = CardOut.from_card(card)

    draw_response = {
        "type": "draw",
        "new_card": card.model_dump(by_alias=True, exclude_unset=True),
        "card_type": card_type,
    }

    return draw_response


@db_session
def handle_exchange(
    exchange_requester: int, chosen_card: int, target_player: int
):
    card = Card.get(id=chosen_card)
    card = CardOut.from_card(card)
    exchange_defense = get_defense_cards(32)
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
    game_id: int,
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
    draw_no_panic(game_id, current_player_id)


@db_session
def exchange_not_defended(
    game_id: int,
    current_player_id: int,
    last_chosen_card: int,
    exchange_requester: int,
    chosen_card: int,
):
    effect = None

    try:
        effect = play(
            id_game=game_id,
            attack_player_id=exchange_requester,
            defense_player_id=current_player_id,
            idtype_attack_card=32,
            idtype_defense_card=0,
            card_chosen_by_attacker=Card.get(id=last_chosen_card).idtype,
            card_chosen_by_defender=Card.get(id=chosen_card).idtype,
        )
    except ValueError as e:
        print("ERROR:", str(e))

    return effect


@db_session
def handle_cannot_exchange(game_id: int):
    calculate_next_turn(game_id)
    game = Game.get(id=game_id)
    game.current_phase = "Draw"
    commit()
    next_player = list(
        filter(lambda p: p.round_position == game.current_position, list(game.players))
    )[0]
    draw_response = draw_card(game_id, next_player.id)
    return draw_response, next_player.id


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

                effect = play(
                    id_game=game_id,
                    attack_player_id=exchange_requester,
                    defense_player_id=current_player_id,
                    idtype_attack_card=32,
                    idtype_defense_card=defense_card.idtype,
                    card_chosen_by_attacker=Card.get(
                        id=last_chosen_card
                    ).idtype,
                )

                exchange_defended(game_id, current_player_id, chosen_card)

            except ValueError as e:
                print("ERROR:", str(e))
        else:
            raise ValueError("Exchange cant be defended with that card")
    else:
        try:
            effect = exchange_not_defended(
                game_id,
                current_player_id,
                last_chosen_card,
                exchange_requester,
                chosen_card,
            )
        except ValueError as e:
            print("ERROR:", str(e))
    calculate_next_turn(game_id)
    player = Player.get(id=exchange_requester)
    player.quarantine = player.quarantine - 1 if player.quarantine > 0 else 0
    commit()
    players = list(game.players)
    next_player = list(
        filter(lambda p: p.round_position == game.current_position, players)
    )[0]
    game.current_phase = "Draw"
    commit()
    try:
        draw_response = draw_card(game_id, next_player.id)
    except ValueError as e:
        print("ERROR:", str(e))

    return draw_response, next_player.id, effect


@db_session
def handle_discard(game_id: int, card_id: int, player_id: int):
    try:
        game = Game.get(id=game_id)
        game.current_phase = "Discard"
        commit()
        gu.discard(game_id, card_id, player_id)
        game.current_phase = "Exchange"
        commit()
    except ValueError as e:
        print("ERROR:", str(e))
