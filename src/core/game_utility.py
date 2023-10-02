"""This module contains the functions that are used to game operation."""
from typing import Optional

from card import add_player_to_card
from card import remove_player_from_card
from card_creation import create_card_asociation
from deck import add_card_to_disposable_deck
from deck import create_available_deck
from deck import create_deck
from deck import create_disposable_deck
from deck import get_deck
from deck import get_random_card_from_available_deck
from deck import move_discard_cards_to_available_deck
from deck import remove_available_deck
from deck import remove_deck
from deck import remove_disposable_deck
from effects import do_effect
from game_action import GameAction
from models.game import Deck
from models.game import Player


def first_deck_creation(id_game: int, cnt_players: int) -> Deck:
    """Create the first deck."""
    create_deck(id_game)
    create_available_deck(id_game, get_deck(id_game))
    create_disposable_deck(id_game, get_deck(id_game))

    create_card_asociation(get_deck(id_game).available_deck, cnt_players)

    return get_deck(id_game)


def draw_card_from_deck(id_game: int, player: Player) -> int:
    """Draw a card from the deck."""
    if len(get_deck(id_game).available_deck.cards) == 0:
        move_discard_cards_to_available_deck(id_game)

    card = get_random_card_from_available_deck(id_game)
    add_player_to_card(card.id, player)
    return card.idtype


def discard_card(id_game: int, id_card_type: int, player: Player) -> None:
    """Discard a card from player hand and add to disposable deck."""
    if player.hand.select(idtype=id_card_type).count() == 0:
        raise ValueError(f"Player with id {player.id} doesn't have this card.")

    card = player.hand.select(idtype=id_card_type).random(1)[0]
    remove_player_from_card(card.id, player)
    add_card_to_disposable_deck(id_game, card)


def play_card(
    id_game: int, id_card_type: int, target: Optional[int] = None
) -> GameAction:
    """Play a card from player hand."""
    return do_effect(id_game, id_card_type, target)


def erase_deck(id_game: int) -> None:
    """Erase the deck."""
    remove_available_deck(id_game)
    remove_disposable_deck(id_game)
    remove_deck(id_game)
