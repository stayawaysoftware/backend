"""Whisky effect."""
import core.effects as effect_aplication
from models.game import Player


def whisky_effect(id_game: int, attack_player_id: int):
    """Whisky effect."""
    # The attack player must to be alive
    if Player[attack_player_id].alive is False:
        raise ValueError("The player with id {attack_player_id} is dead.")

    # Without modifications in the game

    # With message to front

    effect = effect_aplication.show_hand_effect(
        game_id=id_game,
        player_id=attack_player_id,
    )

    return effect
