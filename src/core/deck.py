"""Deck database related functions."""
from models.game import AvailableDeck
from models.game import Card
from models.game import Deck
from models.game import DisposableDeck
from pony.orm import commit
from pony.orm import db_session


def exists_deck(id: int):
    """Check if a deck exists in the database."""
    with db_session:
        return Deck.exists(id=id)


def exists_available_deck(id: int):
    """Check if an available deck exists in the database."""
    with db_session:
        return AvailableDeck.exists(id=id)


def exists_disposable_deck(id: int):
    """Check if a disposable deck exists in the database."""
    with db_session:
        return DisposableDeck.exists(id=id)


def get_deck(id: int):
    """Get a deck from the database."""
    with db_session:
        if exists_deck(id):
            return Deck[id]
        raise ValueError(f"Deck with id {id} doesn't exists.")


def get_available_deck(id: int):
    """Get an available deck from the database."""
    with db_session:
        if exists_available_deck(id):
            return AvailableDeck[id]
        raise ValueError(f"Available deck with id {id} doesn't exists.")


def get_random_card_from_available_deck(id: int):
    """Get a random card from available deck."""
    with db_session:
        if exists_available_deck(id):
            if len(AvailableDeck[id].cards) > 0:
                return AvailableDeck[id].cards.random(1)[0]
            raise ValueError(f"Available deck with id {id} is empty.")
        raise ValueError(f"Available deck with id {id} doesn't exists.")


def get_disposable_deck(id: int):
    """Get a disposable deck from the database."""
    with db_session:
        if exists_disposable_deck(id):
            return DisposableDeck[id]
        raise ValueError(f"Disposable deck with id {id} doesn't exists.")


def create_deck(id: int):
    """Create a deck in the database."""
    with db_session:
        if not exists_deck(id):
            Deck(id=id)
            commit()
        else:
            raise ValueError(f"Deck with id {id} already exists.")


def create_available_deck(id: int, deck: Deck):
    """Create an available deck in the database."""
    with db_session:
        if not exists_available_deck(id):
            AvailableDeck(
                id=id,
                deck=deck,
            )
            commit()
        else:
            raise ValueError(f"Available deck with id {id} already exists.")


def create_disposable_deck(id: int, deck: Deck):
    """Create a disposable deck in the database."""
    with db_session:
        if not exists_disposable_deck(id):
            DisposableDeck(
                id=id,
                deck=deck,
            )
            commit()
        else:
            raise ValueError(f"Disposable deck with id {id} already exists.")


def add_card_to_available_deck(id: int, card: Card):
    """Add a card to an available deck."""
    with db_session:
        if card not in get_available_deck(id).cards:
            get_available_deck(id).cards.add(card)
            commit()
        else:
            raise ValueError(
                f"Card with id {card.id} exists in deck with id {id}."
            )


def add_card_to_disposable_deck(id: int, card: Card):
    """Add a card to a disposable deck."""
    with db_session:
        if card not in get_disposable_deck(id).cards:
            get_disposable_deck(id).cards.add(card)
            commit()
        else:
            raise ValueError(
                f"Card with id {card.id} exists in deck with id {id}."
            )


def remove_card_from_available_deck(id: int, card: Card):
    """Remove a card from an available deck."""
    with db_session:
        if card in get_available_deck(id).cards:
            get_available_deck(id).cards.remove(card)
            commit()
        else:
            raise ValueError(
                f"Card with id {card.id} doesn't exists in deck with id {id}."
            )


def remove_card_from_disposable_deck(id: int, card: Card):
    """Remove a card from a disposable deck."""
    with db_session:
        if card in get_disposable_deck(id).cards:
            get_disposable_deck(id).cards.remove(card)
            commit()
        else:
            raise ValueError(
                f"Card with id {card.id} doesn't exists in deck with id {id}."
            )


def remove_deck(id: int):
    """Remove a deck from the database."""
    with db_session:
        if exists_deck(id):
            Deck[id].delete()
            commit()
        else:
            raise ValueError(f"Deck with id {id} doesn't exists.")


def remove_available_deck(id: int):
    """Remove an available deck from the database."""
    with db_session:
        if exists_available_deck(id):
            AvailableDeck[id].delete()
            commit()
        else:
            raise ValueError(f"Available deck with id {id} doesn't exists.")


def remove_disposable_deck(id: int):
    """Remove a disposable deck from the database."""
    with db_session:
        if exists_disposable_deck(id):
            DisposableDeck[id].delete()
            commit()
        else:
            raise ValueError(f"Disposable deck with id {id} doesn't exists.")
