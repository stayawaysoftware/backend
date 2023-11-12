"""Exchange effect."""
from typing import Optional

from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from models.game import Card
from models.game import Game
from models.game import Player
from pony.orm import db_session
from schemas.card import CardOut


def exchange_effect(
    id_game: int,
    player: int,
    target: Optional[int],
    card_chosen_by_player: Optional[int],
    card_chosen_by_target: Optional[int],
) -> GameAction:
    """Exchange effect."""
    with db_session:
        game = Game[id_game]

        if game.current_phase != "Defense":
            raise ValueError("You can't use this card in this phase.")
        if target is None:
            raise ValueError("You must select a target.")
        if game.players.select(id=target).count() == 0:
            raise ValueError("Target doesn't exists.")
        if not game.players.select(id=target).first().alive:
            raise ValueError("Target is dead.")
        if game.players.select(id=player).count() == 0:
            raise ValueError("Player doesn't exists.")
        if game.players.select(id=player).first().id == target:
            raise ValueError("You can't use this card on yourself.")
        if card_chosen_by_player is None:
            raise ValueError("You must select a card before.")
        if card_chosen_by_target is None:
            raise ValueError("You must select a card before.")

        player_infected = None

        player_role = game.players.select(id=player).first().role
        target_role = game.players.select(id=target).first().role

        player_hand = list(game.players.select(id=player).first().hand)
        target_hand = list(game.players.select(id=target).first().hand)

        player_cnt_infected_cards = 0
        target_cnt_infected_cards = 0

        for card in player_hand:
            if card.idtype == 2:
                player_cnt_infected_cards += 1

        for card in target_hand:
            if card.idtype == 2:
                target_cnt_infected_cards += 1

        if card_chosen_by_player == 1 or card_chosen_by_target == 1:
            raise ValueError("You can't exchange The Thing card.")

        if card_chosen_by_player == 2 and card_chosen_by_target == 2:
            raise ValueError(
                "You can't exchange Infected card from both sides."
            )

        elif card_chosen_by_player == 2:
            if player_role == "The Thing":
                if target_role == "Infected":
                    raise ValueError(
                        f"Player with id {player} can't exchange Infected card with another Infected player."
                    )

                elif target_role == "Human":
                    player_infected = target

            elif player_role == "Infected":
                if player_cnt_infected_cards == 1:
                    raise ValueError(
                        f"Player with id {player} can't exchange Infected card because he has only one Infected card."
                    )

                if target_role == "The Thing":
                    pass  # Nothing to do

                elif target_role == "Infected" or target_role == "Human":
                    raise ValueError(
                        f"Player with id {player} can't exchange Infected card with another Infected or Human player."
                    )

            elif player_role == "Human":
                raise ValueError(
                    f"Player with id {player} can't exchange Infected card because he's an human."
                )

        elif card_chosen_by_target == 2:
            if target_role == "The Thing":
                if player_role == "Infected":
                    raise ValueError(
                        f"Player with id {target} can't exchange Infected card with another Infected player."
                    )

                elif player_role == "Human":
                    player_infected = player

            elif target_role == "Infected":
                if target_cnt_infected_cards == 1:
                    raise ValueError(
                        f"Player with id {target} can't exchange Infected card because he has only one Infected card."
                    )

                if player_role == "The Thing":
                    pass

                elif player_role == "Infected" or player_role == "Human":
                    raise ValueError(
                        f"Player with id {target} can't exchange Infected card with another Infected or Human player."
                    )

            elif target_role == "Human":
                raise ValueError(
                    f"Player with id {target} can't exchange Infected card because he's an human."
                )

        if player_infected is None:
            return GameAction(
                action=ActionType.EXCHANGE,
                target=[player, target],
                card_target=[card_chosen_by_player, card_chosen_by_target],
                exchange_phase=False,
            )
        else:
            return GameAction(
                action=ActionType.EXCHANGE,
                action2=ActionType.INFECT,
                target=[player, target, player_infected],
                card_target=[card_chosen_by_player, card_chosen_by_target],
                exchange_phase=False,
            )


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
        Card.select(idtype=card_chosen_by_attacker).first()
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


def you_failed_effect(
    id_game: int,
    player: int,
    target: Optional[int],
    card_chosen_by_target: Optional[int],
) -> GameAction:
    """You failed effect."""
    with db_session:
        game = Game[id_game]

        if game.current_phase != "Defense":
            raise ValueError("You can't use this card in this phase.")
        if target is None:
            raise ValueError("You must select a target.")
        if game.players.select(id=target).count() == 0:
            raise ValueError("Target doesn't exists.")
        if not game.players.select(id=target).first().alive:
            raise ValueError("Target is dead.")
        if game.players.select(id=player).count() == 0:
            raise ValueError("Player doesn't exists.")
        if game.players.select(id=player).first().id == target:
            raise ValueError("You can't use this card on yourself.")
        if card_chosen_by_target is None:
            raise ValueError("You must select a card before.")

        return GameAction(
            action=ActionType.ASK_EXCHANGE,
            target=[target, player],
            card_target=[card_chosen_by_target],
        )
