"""Function of play phase."""
from typing import Optional

from core.game_logic.effects.effect_handler import do_effect_defense
from core.game_logic.game_utility import get_defense_cards
from models.game import Card
from models.game import Game
from models.game import Player
from pony.orm import db_session


# Play function of defense phase (to returns an effect)


@db_session
def play(
    id_game: int,
    attack_player_id: int,
    defense_player_id: int,
    idtype_attack_card: int,
    idtype_defense_card: int,
    card_chosen_by_attacker: Optional[int] = None,
    card_chosen_by_defender: Optional[int] = None,
):
    """Play a combination of cards between attacker and defender players."""

    # Game doesn't exist
    if not Game.exists(id=id_game):
        raise ValueError(f"Game with id {id_game} doesn't exist")

    # Player doesn't exist
    if not Player.exists(id=attack_player_id):
        raise ValueError(f"Player with id {attack_player_id} doesn't exist")
    if not Player.exists(id=defense_player_id):
        raise ValueError(f"Player with id {defense_player_id} doesn't exist")

    # Card is not in hand
    if (
        idtype_attack_card not in [0, 32]
        and Player[attack_player_id]
        .hand.select(idtype=idtype_attack_card)
        .count()
        == 0
    ):
        raise ValueError(
            f"Player with id {attack_player_id} has no card with idtype {idtype_attack_card} in hand"
        )
    if (
        idtype_defense_card not in [0, 32]
        and Player[defense_player_id]
        .hand.select(idtype=idtype_defense_card)
        .count()
        == 0
    ):
        raise ValueError(
            f"Player with id {defense_player_id} has no card with idtype {idtype_defense_card} in hand"
        )
    if (
        card_chosen_by_attacker is not None
        and Player[attack_player_id]
        .hand.select(idtype=card_chosen_by_attacker)
        .count()
        == 0
    ):
        raise ValueError(
            f"Player with id {attack_player_id} has no card with idtype {card_chosen_by_attacker} in hand"
        )
    if (
        card_chosen_by_defender is not None
        and Player[defense_player_id]
        .hand.select(idtype=card_chosen_by_defender)
        .count()
        == 0
    ):
        raise ValueError(
            f"Player with id {defense_player_id} has no card with idtype {card_chosen_by_defender} in hand"
        )

    # The Thing and Infected cards cannot be played
    if idtype_attack_card == 1 or idtype_defense_card == 1:
        raise ValueError("The Thing cannot be played")
    if idtype_attack_card == 2 or idtype_defense_card == 2:
        raise ValueError("Infected cannot be played")

    # Defense card must to be of Defense type
    if (
        idtype_defense_card != 0
        and idtype_defense_card not in get_defense_cards(idtype_attack_card)
    ):
        raise ValueError(
            f"Card with idtype {idtype_defense_card} cannot be played as defense to card with idtype {idtype_attack_card}"
        )
    if (
        idtype_attack_card != 32
        and Card.select(idtype=idtype_attack_card).first().type == "DEFENSE"
    ):
        raise ValueError(
            f"Card with idtype {idtype_attack_card} cannot be played as attack"
        )

    # Call do_effect method to do the modifications of the game

    return do_effect_defense(
        id_game=id_game,
        attack_player_id=attack_player_id,
        defense_player_id=defense_player_id,
        idtype_attack_card=idtype_attack_card,
        idtype_defense_card=idtype_defense_card,
        card_chosen_by_attacker=card_chosen_by_attacker,
        card_chosen_by_defender=card_chosen_by_defender,
    )
