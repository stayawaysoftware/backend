"""Functions used to all the game operation (internal logic)."""
from core.game_logic.card import get_card
from core.game_logic.card import relate_card_with_available_deck
from core.game_logic.card import relate_card_with_disposable_deck
from core.game_logic.card import relate_card_with_player
from core.game_logic.card import unrelate_card_with_available_deck
from core.game_logic.card import unrelate_card_with_disposable_deck
from core.game_logic.card import unrelate_card_with_player
from core.game_logic.card_creation import card_defense
from core.game_logic.card_creation import init_available_deck
from core.game_logic.deck import create_available_deck
from core.game_logic.deck import create_deck
from core.game_logic.deck import create_disposable_deck
from core.game_logic.deck import delete_available_deck
from core.game_logic.deck import delete_deck
from core.game_logic.deck import delete_disposable_deck
from core.game_logic.deck import get_deck
from core.game_logic.deck import get_random_card_from_available_deck
from core.game_logic.deck import get_specific_card_from_available_deck
from core.game_logic.deck import get_specific_card_from_disposable_deck
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


# Initialization of player's hand (start of the game)


def get_initial_player_hand(id_game: int, id_player: int) -> None:
    """Initialize the player's hand."""
    with db_session:
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")

    cnt_assigned_cards = 0

    if len(get_deck(id_game).available_deck.cards.filter(idtype=1)) > 0:
        card = draw_specific(id_game, id_player, 1)
        card_idtype = get_card(card).idtype
        cnt_assigned_cards += 1

    cards_to_restore = []

    while cnt_assigned_cards < 4:
        card = draw_no_panic(id_game, id_player)
        card_idtype = get_card(card).idtype

        if card_idtype == 2:
            unrelate_card_with_player(card, id_player)
            cards_to_restore.append(card)
        else:
            cnt_assigned_cards += 1

    # Restore the cards that are of type 2 (PANIC)
    for card in cards_to_restore:
        relate_card_with_available_deck(card, id_game)


# Delete decks (end of the game)


def delete_decks(id_game: int) -> None:
    """Delete the decks of the game."""
    delete_deck(id_game)
    delete_available_deck(id_game)
    delete_disposable_deck(id_game)


# Get defense cards


def get_defense_cards(idtype_card: int) -> list[int]:
    """Return the list of cards that can be used as defense."""
    if idtype_card not in range(0, 33):
        raise ValueError(f"idtype_card {idtype_card} is not in range [0, 32]")

    return card_defense[idtype_card]


# ===================== GAME PHASES OF DECK LOGIC =====================

# DRAW phase


def draw(id_game: int, id_player: int) -> int:
    """Draw a card from the available deck."""
    with db_session:
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")
        if Game[id_game].current_phase != "Draw":
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


def draw_specific(id_game: int, id_player: int, idtype_card: int) -> int:
    """Draw a specific card from the available or disposable deck."""
    with db_session:
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")

    # I've got the card from one of the two decks

    get_functions = [
        get_specific_card_from_available_deck,
        get_specific_card_from_disposable_deck,
    ]
    card = None

    for index in range(2):
        try:
            card = get_functions[index](id_game, idtype_card)
        except ValueError:
            card = None

        if card is not None:
            break

    if card is None:
        raise ValueError(
            f"Decks of game with id {id_game} doesn't have a card with idtype {idtype_card}"
        )

    # I make the corresponding associations with this card obtained

    unrelate_functions = [
        unrelate_card_with_available_deck,
        unrelate_card_with_disposable_deck,
    ]
    unrelate_functions[index](card.id, id_game)
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
