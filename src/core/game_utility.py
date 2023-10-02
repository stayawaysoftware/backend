"""This module contains the functions that are used to game operation."""
from card_creation import create_card_asociation
from deck import create_available_deck
from deck import create_deck
from deck import create_disposable_deck
from deck import get_deck


def first_deck_creation(id_game: int, cnt_players: int):
    """Create the first deck."""
    create_deck(id_game)
    create_available_deck(id_game, get_deck(id_game))
    create_disposable_deck(id_game, get_deck(id_game))

    create_card_asociation(get_deck(id_game).available_deck, cnt_players)

    return get_deck(id_game)
