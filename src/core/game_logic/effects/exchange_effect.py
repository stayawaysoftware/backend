"""Exchange effect."""
from typing import Optional

from core.game_logic.effects.nothing_effect import nothing_effect
from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from models.game import Game
from pony.orm import db_session


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


def terrifying_effect(
    id_game: int,
    player: int,
    target: Optional[int],
    card_chosen_by_target: Optional[int],
) -> GameAction:
    """Terrifying effect."""
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
            action=ActionType.SHOW,
            target=[target, player],
            card_target=[card_chosen_by_target],
        )


def no_thanks_effect(id_game: int) -> GameAction:
    """No thanks effect."""
    with db_session:
        game = Game[id_game]

        if game.current_phase != "Defense":
            raise ValueError("You can't use this card in this phase.")

        return nothing_effect(id_game)


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
