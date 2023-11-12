"""Analysis Effect."""
from core.player import get_alive_neighbors
from models.game import Player
from schemas.card import CardOut


def analysis_effect(
    id_game: int, attack_player_id: int, defense_player_id: int
):
    """Analysis effect."""

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
    # With effects to show in the frontend

    card_list_to_show = [
        CardOut.from_card(card) for card in Player[defense_player_id].hand
    ]

    effect = {
        "type": "show_card",
        "player_name": Player[defense_player_id].name,
        "target": [attack_player_id],
        "cards": [
            card.dict(by_alias=True, exclude_unset=True)
            for card in card_list_to_show
        ],
    }

    return effect
