"""Analysis Effect."""
from typing import Optional

from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from models.game import Game
from pony.orm import db_session


def analysis_effect(
    id_game: int, id_player: int, target: Optional[int]
) -> GameAction:
    """Analysis effect."""
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
        if game.players.select(id=id_player).count() == 0:
            raise ValueError("Player doesn't exists.")
        if game.players.select(id=id_player).first().id == target:
            raise ValueError("You can't use this card on yourself.")

        return GameAction(
            action=ActionType.SHOW_ALL, target=[target, id_player]
        )
