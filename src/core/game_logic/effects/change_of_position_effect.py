"""Change of position effect."""

from typing import Optional

from core.game_logic.effects.nothing_effect import nothing_effect
from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from models.game import Game
from pony.orm import db_session

def change_of_position_effect(
    id_game: int,
    player: int,
    target: Optional[int],
) -> GameAction:
    """Change of position effect."""
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

        return GameAction(
            action=ActionType.CHANGE_POSITION, target=[target, player]
        )


def im_fine_here_effect(id_game: int) -> GameAction:
    """I'm fine here effect."""
    with db_session:
        game = Game[id_game]

        if game.current_phase != "Defense":
            raise ValueError("You can't use this card in this phase.")

        return nothing_effect(id_game)
