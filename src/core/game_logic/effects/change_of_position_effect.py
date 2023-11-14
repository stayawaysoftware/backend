"""Change of position effect."""
import core.effects as effect_aplication
from core.player import get_alive_neighbors
from models.game import Player


def change_of_position_effect(
    id_game: int, attack_player_id: int, defense_player_id: int
):
    """Change of position effect."""

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
    # Swap positions
    # Set current position to the attack player position

    # Without effects to show in the frontend

    effect = effect_aplication.position_change_effect(
        game_id=id_game,
        target_id=defense_player_id,
        user_id=attack_player_id,
    )


def you_better_run_effect(
    id_game: int, attack_player_id: int, defense_player_id: int
):
    """Change of position effect."""

    # The defense player must to be alive
    if Player[defense_player_id].alive is False:
        raise ValueError("The player with id {defense_player_id} is dead.")

    # With modifications in the game
    # Swap positions
    # Set current position to the attack player position

    # Without effects to show in the frontend

    effect = effect_aplication.position_change_effect(
        game_id=id_game,
        target_id=defense_player_id,
        user_id=attack_player_id,
    )

    return effect


def im_fine_here_effect(defense_player_id: int):
    """I'm fine here effect."""

    if Player[defense_player_id].alive is False:
        raise ValueError("The player with id {defense_player_id} is dead.")

    # Without modifications in the game and without effects to show in the frontend

    effect = None

    return effect
