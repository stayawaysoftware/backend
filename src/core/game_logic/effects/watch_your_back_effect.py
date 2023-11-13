"""Watch your back effect."""
from models.game import Game
from pony.orm import commit
from pony.orm import db_session


@db_session
def watch_your_back_effect(id_game: int):
    """Watch your back effect."""

    # With modifications in the game

    Game[id_game].round_left_direction ^= 1
    commit()

    # Without effects to show in the frontend

    return None
