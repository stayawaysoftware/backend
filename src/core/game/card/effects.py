"""All card effects."""

from src.core.game.game import Game
from src.core.game.game_action import GameAction

def flamethrower_effect(game: Game, target: int = None) -> GameAction:
    """Flamethrower effect."""
    assert game.get_actual_phase() == "PLAY" and target is not None \
        and game.get_actual_turn() != target and game.get_player_quantity() > 1
    return GameAction("KILL", target)
