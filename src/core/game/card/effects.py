"""All card effects."""

from src.core.game.game import Game
from src.core.game.game_action import GameAction

def flamethrower_effect(game: Game, target: int = None) -> GameAction:
    """Flamethrower effect."""
    assert target is not None and game.get_player_quantity() > 1
    return GameAction("KILL", target)
