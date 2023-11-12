"""Flamethrower effect."""
from typing import Optional

from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from models.game import Game
from models.game import Player
from pony.orm import db_session


def flamethrower_effect(id_game: int, target: Optional[int]) -> GameAction:
    """Flamethrower effect."""
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

        return GameAction(action=ActionType.KILL, target=[target])


@db_session
def no_barbecues_effect(defense_player_id: int):
    """No barbecues effect."""

    if Player[defense_player_id].alive is False:
        raise ValueError("The player with id {defense_player_id} is dead.")

    # Without modifications in the game and without effects to show in the frontend

    return None
