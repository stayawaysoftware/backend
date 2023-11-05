"""Suspicion effect."""
from typing import Optional

from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from models.game import Game
from pony.orm import db_session


def suspicion_effect(
    id_game: int,
    player: int,
    target: Optional[int],
    card_chosen_by_player: Optional[int],
) -> GameAction:
    """Suspicion effect."""
    with db_session:
        game = Game[id_game]

        if game.current_phase != "Play":
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
        if (
            game.players.select(id=target)
            .first()
            .hand.select(idtype=card_chosen_by_player)
            .count()
            == 0
        ):
            raise ValueError(
                f"Target doesn't have this card with id {card_chosen_by_player}"
            )

        return GameAction(
            action=ActionType.SHOW,
            target=[target, player],
            card_target=[card_chosen_by_player],
        )
