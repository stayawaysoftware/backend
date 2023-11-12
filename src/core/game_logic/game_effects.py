"""Function of play phase."""
from typing import Optional

from core.game_logic.card_creation import card_defense
from core.game_logic.effects.effect_handler import do_effect
from models.game import Game
from models.game import Player
from pony.orm import db_session


# Get defense cards


def get_defense_cards(idtype_card: int) -> list[int]:
    """Return the list of cards that can be used as defense."""
    if idtype_card not in range(0, 33):
        raise ValueError(f"idtype_card {idtype_card} is not in range [0, 32]")

    return card_defense[idtype_card]


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

    # Game is not in the Defense phase
    if Game[id_game].current_phase != "Defense":
        raise ValueError(f"Game with id {id_game} is not in the Defense phase")

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

    # Call do_effect method to do the modifications of the game

    # TODO: Add parameters to do_effect
    return do_effect()
