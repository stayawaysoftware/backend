"""Whisky effect."""
from models.game import Game
from models.game import Player
from schemas.card import CardOut


def whisky_effect(id_game: int, attack_player_id: int):
    """Whisky effect."""
    # The attack player must to be alive
    if Player[attack_player_id].alive is False:
        raise ValueError("The player with id {attack_player_id} is dead.")

    # Without modifications in the game

    # With message to front

    card_list_to_show = [
        CardOut.from_card(card) for card in Player[attack_player_id].hand
    ]

    player_list_to_show = sorted(
        player.id
        for player in Game[id_game].players
        if player.id != attack_player_id
    )

    effect = {
        "type": "show_card",
        "player_name": Player[attack_player_id].name,
        "target": player_list_to_show,
        "cards": [
            card.dict(by_alias=True, exclude_unset=True)
            for card in card_list_to_show
        ],
    }

    return effect
