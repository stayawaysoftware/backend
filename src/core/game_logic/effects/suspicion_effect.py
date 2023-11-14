"""Suspicion effect."""
import core.effects as effect_aplication
from core.player import get_alive_neighbors
from models.game import Player


def suspicion_effect(
    id_game: int, attack_player_id: int, defense_player_id: int
):
    """Suspicion effect."""

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

    # Without modifications in the game

    # With effects to show in the frontend - Get a random card to show

    effect = effect_aplication.sospecha_effect(
        game_id=id_game,
        target_id=defense_player_id,
        user_id=attack_player_id,
    )

    return effect
