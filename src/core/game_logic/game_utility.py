"""Functions used to all the game operation (internal logic)."""
from core.game_logic.card import relate_card_with_disposable_deck
from core.game_logic.card import relate_card_with_player
from core.game_logic.card import unrelate_card_with_available_deck
from core.game_logic.card import unrelate_card_with_player
from core.game_logic.card_creation import init_available_deck
from core.game_logic.deck import create_available_deck
from core.game_logic.deck import create_deck
from core.game_logic.deck import create_disposable_deck
from core.game_logic.deck import delete_available_deck
from core.game_logic.deck import delete_deck
from core.game_logic.deck import delete_disposable_deck
from core.game_logic.deck import get_deck
from core.game_logic.deck import get_random_card_from_available_deck
from core.game_logic.deck import move_disposable_to_available_deck
from models.game import Deck
from models.game import Game
from models.game import Player
from pony.orm import db_session

# ===================== BASIC GAME FUNCTIONS =====================

# Initialization of decks (start of the game)


def initialize_decks(id_game: int, quantity_players: int) -> Deck:
    """Initialize the decks of the game."""
    create_deck(id_game)
    create_available_deck(id_game)
    create_disposable_deck(id_game)

    init_available_deck(id_game, quantity_players)

    return get_deck(id_game)


# Delete decks (end of the game)


def delete_decks(id_game: int) -> None:
    """Delete the decks of the game."""
    delete_deck(id_game)
    delete_available_deck(id_game)
    delete_disposable_deck(id_game)


# ===================== GAME PHASES OF DECK LOGIC =====================

# DRAW phase


def draw(id_game: int, id_player: int) -> int:
    """Draw a card from the available deck."""
    with db_session:
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")
        if Game[1].current_phase != "Draw":
            raise ValueError(
                f"Game with id {id_game} is not in the Draw phase"
            )

    if len(get_deck(id_game).available_deck.cards) == 0:
        move_disposable_to_available_deck(id_game)

    card = get_random_card_from_available_deck(id_game)
    unrelate_card_with_available_deck(card.id, id_game)
    relate_card_with_player(card.id, id_player)
    return card.id


def draw_no_panic(id_game: int, id_player: int) -> int:
    """Draw a card from the available deck. The card isn't of panic type."""
    with db_session:
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")

        if len(get_deck(id_game).available_deck.cards) == 0:
            move_disposable_to_available_deck(id_game)

        card = get_random_card_from_available_deck(id_game)
        while card.type == "PANIC":
            unrelate_card_with_available_deck(card.id, id_game)
            relate_card_with_disposable_deck(card.id, id_game)

            if len(get_deck(id_game).available_deck.cards) == 0:
                move_disposable_to_available_deck(id_game)

            card = get_random_card_from_available_deck(id_game)

        unrelate_card_with_available_deck(card.id, id_game)
        relate_card_with_player(card.id, id_player)

        return card.id


# DISCARD phase


def discard(id_game: int, idtype_card: int, id_player: int) -> int:
    """Discard a card from player hand."""
    with db_session:
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")
        if Game[id_game].current_phase != "Discard":
            raise ValueError(
                f"Game with id {id_game} is not in the Discard phase"
            )
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if len(Player[id_player].hand) == 0:
            raise ValueError(
                f"Player with id {id_player} has no cards in hand"
            )
        if len(Player[id_player].hand.select(idtype=idtype_card)) == 0:
            raise ValueError(
                f"Player with id {id_player} has no card with idtype {idtype_card} in hand"
            )

        card = Player[id_player].hand.select(idtype=idtype_card).random(1)[0]

    unrelate_card_with_player(card.id, id_player)
    relate_card_with_disposable_deck(card.id, id_game)

    return card.id
