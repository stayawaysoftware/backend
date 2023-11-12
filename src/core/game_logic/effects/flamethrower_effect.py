"""Flamethrower effect."""
from core.player import get_alive_neighbors
from models.game import Player
from pony.orm import commit
from pony.orm import db_session


@db_session
def flamethrower_effect(
    id_game: int, attack_player_id: int, defense_player_id: int
):
    """Flamethrower effect."""

    # The defense player must to be alive
    if Player[defense_player_id].alive is False:
        raise ValueError("The player with id {defense_player_id} is dead.")

    # The defense player must to be neighbor of the attack player
    attack_neighbors = get_alive_neighbors(
        id_game=id_game, id_player=attack_player_id
    )
    if defense_player_id not in attack_neighbors:
        raise ValueError(
            "The player with id {defense_player_id} is not a neighbor of the player with id {attack_player_id}."
        )

    # With modifications in the game

    Player[defense_player_id].alive = False
    commit()

    # Without effects to show in the frontend

    return None


@db_session
def no_barbecues_effect(defense_player_id: int):
    """No barbecues effect."""

    if Player[defense_player_id].alive is False:
        raise ValueError("The player with id {defense_player_id} is dead.")

    # Without modifications in the game and without effects to show in the frontend

    return None
