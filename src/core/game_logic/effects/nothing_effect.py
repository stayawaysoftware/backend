"""Nothing effect."""
from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from pony.orm import db_session


def nothing_effect(id_game: int) -> GameAction:
    """Nothing effect."""
    with db_session:
        return GameAction(action=ActionType.NOTHING)
