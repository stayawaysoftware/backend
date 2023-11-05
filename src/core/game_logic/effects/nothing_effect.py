"""Nothing effect."""

from pony.orm import db_session
from src.core.game_logic.game_action import ActionType
from src.core.game_logic.game_action import GameAction

def nothing_effect(id_game: int) -> GameAction:
    """Nothing effect."""
    with db_session:
        return GameAction(action=ActionType.NOTHING)
    