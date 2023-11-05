"""Deck database related functions."""
from core.game_logic.card import relate_card_with_available_deck
from core.game_logic.card import unrelate_card_with_disposable_deck
from models.game import AvailableDeck
from models.game import Card
from models.game import Deck
from models.game import DisposableDeck
from pony.orm import commit
from pony.orm import db_session

# ===================== BASIC DECK FUNCTIONS =====================


# Exists
def exists_deck(id: int) -> bool:
    """Check if a deck exists in the database"""
    with db_session:
        return Deck.exists(id=id)


def exists_available_deck(id: int) -> bool:
    """Check if an available deck exists in the database"""
    with db_session:
        return AvailableDeck.exists(id=id)


def exists_disposable_deck(id: int) -> bool:
    """Check if a disposable deck exists in the database"""
    with db_session:
        return DisposableDeck.exists(id=id)


# Get
def get_deck(id: int) -> Deck:
    """Get a deck from the database"""
    with db_session:
        if exists_deck(id):
            return Deck[id]
        raise ValueError(f"Deck with id {id} doesn't exist")


def get_available_deck(id: int) -> AvailableDeck:
    """Get an available deck from the database"""
    with db_session:
        if exists_available_deck(id):
            return AvailableDeck[id]
        raise ValueError(f"Available deck with id {id} doesn't exist")


def get_disposable_deck(id: int) -> DisposableDeck:
    """Get a disposable deck from the database"""
    with db_session:
        if exists_disposable_deck(id):
            return DisposableDeck[id]
        raise ValueError(f"Disposable deck with id {id} doesn't exist")


# Create


def create_deck(id: int) -> Deck:
    """Create a deck in the database"""
    with db_session:
        if not exists_deck(id):
            deck = Deck(id=id)
            commit()
            return deck
        raise ValueError(f"Deck with id {id} already exists")


def create_available_deck(id: int) -> AvailableDeck:
    """Create an available deck in the database and related with deck"""
    with db_session:
        if not exists_available_deck(id):
            deck = get_deck(id)
            available_deck = AvailableDeck(id=id, deck=deck)
            commit()
            return available_deck
        raise ValueError(f"Available deck with id {id} already exists")


def create_disposable_deck(id: int) -> DisposableDeck:
    """Create a disposable deck in the database and related with deck"""
    with db_session:
        if not exists_disposable_deck(id):
            deck = get_deck(id)
            disposable_deck = DisposableDeck(id=id, deck=deck)
            commit()
            return disposable_deck
        raise ValueError(f"Disposable deck with id {id} already exists")


# ===================== DECK-CARD FUNCTIONS =====================

# Get cards


def get_random_card_from_available_deck(id_available_deck: int) -> Card:
    """Get a random card from an available deck"""
    with db_session:
        available_deck = get_available_deck(id_available_deck)
        if len(available_deck.cards) > 0:
            return available_deck.cards.random(1)[0]
        raise ValueError(
            f"Available deck with id {id_available_deck} is empty"
        )


# Move cards


def move_disposable_to_available_deck(id: int) -> None:
    """
    Move all cards from disposable deck to available deck
    Pre: SZ(disposable_deck) > 0 and SZ(available_deck) = 0
    """
    with db_session:
        disposable_deck = get_disposable_deck(id)
        available_deck = get_available_deck(id)

        if len(disposable_deck.cards) > 0 and len(available_deck.cards) == 0:
            disposable_cards = list(disposable_deck.cards)
            for card in disposable_cards:
                unrelate_card_with_disposable_deck(card.id, id)
                relate_card_with_available_deck(card.id, id)
        else:
            raise ValueError(
                f"Disposable deck with id {id} is empty or available deck with id {id} is not empty"
            )


# ===================== DELETE DECK FUNCTIONS =====================


def delete_deck(id: int) -> None:
    """Delete a deck from the database"""
    with db_session:
        if exists_deck(id):
            Deck[id].delete()
            commit()
        else:
            raise ValueError(f"Deck with id {id} doesn't exist")


def delete_available_deck(id: int) -> None:
    """Delete an available deck from the database"""
    with db_session:
        if exists_available_deck(id):
            AvailableDeck[id].delete()
            commit()
        else:
            raise ValueError(f"Available deck with id {id} doesn't exist")


def delete_disposable_deck(id: int) -> None:
    """Delete a disposable deck from the database"""
    with db_session:
        if exists_disposable_deck(id):
            DisposableDeck[id].delete()
            commit()
        else:
            raise ValueError(f"Disposable deck with id {id} doesn't exist")
