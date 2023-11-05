"""Watch your back effect."""
from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from models.game import Game
from pony.orm import db_session


def watch_your_back_effect(id_game: int, player: int) -> GameAction:
    """Watch your back effect."""
    with db_session:
        game = Game[id_game]

        if game.current_phase != "Play":
            raise ValueError("You can't use this card in this phase.")
        if game.players.select(id=player).count() == 0:
            raise ValueError("Player doesn't exists.")

        return GameAction(action=ActionType.REVERSE_ORDER)
