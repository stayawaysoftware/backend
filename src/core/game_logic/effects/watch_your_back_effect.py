"""Watch your back effect."""
import core.effects as effect_aplication
from pony.orm import db_session


@db_session
def watch_your_back_effect(id_game: int):
    """Watch your back effect."""

    # With modifications in the game
    # Without effects to show in the frontend

    effect = effect_aplication.vigila_tus_espaldas_effect(game_id=id_game)

    return effect
