"""Exchange effect."""
from typing import Optional

from core.game_logic.card import relate_card_with_player
from core.game_logic.card import unrelate_card_with_player
from core.player import get_alive_neighbors
from models.game import Player
from pony.orm import db_session
from schemas.card import CardOut


@db_session
def exchange_effect(
    id_game: int,
    attack_player_id: int,
    defense_player_id: Optional[int],
    card_chosen_by_attacker: Optional[int],
    card_chosen_by_defender: Optional[int],
):
    """Exchange effect."""

    # The two players must be alive

    if Player[attack_player_id].alive is False:
        raise ValueError("The player with id {attack_player_id} is dead.")
    if Player[defense_player_id].alive is False:
        raise ValueError("The player with id {defense_player_id} is dead.")

    # The defense player must to be neighbor of the attack player

    attack_neighbors = get_alive_neighbors(
        id_game=id_game, id_player=attack_player_id
    )
    if defense_player_id not in attack_neighbors:
        raise ValueError(
            "The player with id {defense_player_id} is not a neighbor of the player with id {attack_player_id}."
        )

    # The cards chosen by the attacker and the defender must be not None

    if card_chosen_by_attacker is None:
        raise ValueError("The attacker must choose a card.")
    if card_chosen_by_defender is None:
        raise ValueError("The defender must choose a card.")

    # Do the exchange

    # Calculate important values to do the exchange and check if the exchange is possible

    player_infected = None

    attack_player_role = Player[attack_player_id].role
    defense_player_role = Player[defense_player_id].role

    attack_player_hand = list(Player[attack_player_id].hand)
    defense_player_hand = list(Player[defense_player_id].hand)

    attack_player_cnt_infection_cards = 0
    defense_player_cnt_infection_cards = 0

    for card in attack_player_hand:
        if card.idtype == 2:
            attack_player_cnt_infection_cards += 1

    for card in defense_player_hand:
        if card.idtype == 2:
            defense_player_cnt_infection_cards += 1

    # Check if the exchange is possible

    # You can't exchange The Thing card
    if card_chosen_by_attacker == 1 or card_chosen_by_defender == 1:
        raise ValueError("You can't exchange The Thing card.")

    # You can't exchange the Infection card from both sides
    if card_chosen_by_attacker == 2 and card_chosen_by_defender == 2:
        raise ValueError(
            "You can't exchange the Infection card from both sides."
        )
    elif card_chosen_by_attacker == 2:
        # Attacker is The Thing
        if attack_player_role == "The Thing":

            if defense_player_role == "Infected":
                # Attacker is The Thing and defender is Infected
                raise ValueError(
                    "The Thing player can't exchange the Infection card with the Infected player."
                )
            elif defense_player_role == "Human":
                # Attacker is The Thing and defender is Human
                player_infected = defense_player_id

        # Attacker is Infected
        elif attack_player_role == "Infected":
            if attack_player_cnt_infection_cards == 1:
                # Attacker is Infected and has only one Infection card
                raise ValueError(
                    "The Infected player can't exchange the Infection card if he has only one Infection card."
                )

            if (
                defense_player_role == "Infected"
                or defense_player_role == "Human"
            ):
                # Attacker is Infected and defender is Infected or Human
                raise ValueError(
                    f"Player with id {attack_player_id} can't exchange Infected card with another Infected or Human player."
                )

    elif card_chosen_by_defender == 2:
        # Defender is The Thing
        if defense_player_role == "The Thing":

            if attack_player_role == "Infected":
                # Defender is The Thing and attacker is Infected
                raise ValueError(
                    "The Thing player can't exchange the Infection card with the Infected player."
                )
            elif attack_player_role == "Human":
                # Defender is The Thing and attacker is Human
                player_infected = attack_player_id

        # Defender is Infected
        elif defense_player_role == "Infected":
            if defense_player_cnt_infection_cards == 1:
                # Defender is Infected and has only one Infection card
                raise ValueError(
                    "The Infected player can't exchange the Infection card if he has only one Infection card."
                )

            if (
                attack_player_role == "Infected"
                or attack_player_role == "Human"
            ):
                # Defender is Infected and attacker is Infected or Human
                raise ValueError(
                    f"Player with id {defense_player_id} can't exchange Infected card with another Infected or Human player."
                )

    # Do the exchange because it's possible

    # Exchange the cards

    id_chosen_attacker_card, id_chosen_defender_card = None, None

    for card in attack_player_hand:
        if card.idtype == card_chosen_by_attacker:
            if (
                id_chosen_attacker_card is None
                or id_chosen_attacker_card > card.id
            ):
                id_chosen_attacker_card = card.id

    for card in defense_player_hand:
        if card.idtype == card_chosen_by_defender:
            if (
                id_chosen_defender_card is None
                or id_chosen_defender_card > card.id
            ):
                id_chosen_defender_card = card.id

    unrelate_card_with_player(id_chosen_attacker_card, attack_player_id)
    unrelate_card_with_player(id_chosen_defender_card, defense_player_id)

    relate_card_with_player(id_chosen_attacker_card, defense_player_id)
    relate_card_with_player(id_chosen_defender_card, attack_player_id)

    # Set the infection player
    if player_infected is not None:
        Player[player_infected].role = "Infected"

    # Without effects to show in the frontend

    return None


@db_session
def terrifying_effect(
    attack_player_id: int,
    defense_player_id: int,
    card_chosen_by_attacker: Optional[int],
):
    """Terrifying effect."""

    # The card that attacker wanted to exchange must be not None

    if card_chosen_by_attacker is None:
        raise ValueError(
            "For terrifying effect, the attacker must choose a card."
        )

    # The two players must be alive

    if Player[attack_player_id].alive is False:
        raise ValueError("The player with id {attack_player_id} is dead.")
    if Player[defense_player_id].alive is False:
        raise ValueError("The player with id {defense_player_id} is dead.")

    # Without modifications in the game !!!

    # With effects to show in the frontend !!!

    card_to_show = CardOut.from_card(
        Player[attack_player_id]
        .hand.select(idtype=card_chosen_by_attacker)
        .first()
    )

    effect = {
        "type": "show_card",
        "player_name": Player[attack_player_id].name,
        "target": [defense_player_id],
        "cards": [card_to_show.dict(by_alias=True, exclude_unset=True)],
    }

    return effect


@db_session
def no_thanks_effect(defense_player_id: int):
    """No thanks effect."""

    if Player[defense_player_id].alive is False:
        raise ValueError("The player with id {defense_player_id} is dead.")

    # Without modifications in the game and without effects to show in the frontend

    return None
