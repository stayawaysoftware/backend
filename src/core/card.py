"""Card database related functions."""
from models.game import AvailableDeck
from models.game import Card
from models.game import DisposableDeck
from models.game import Player
from pony.orm import commit
from pony.orm import db_session


def exists_card(id: int):
    """Check if a card exists in the database."""
    with db_session:
        return Card.exists(id=id)


def get_card(id: int):
    """Get a card from the database."""
    with db_session:
        if exists_card(id):
            return Card[id]
        raise ValueError(f"Card with id {id} doesn't exists.")


def create_card(id: int, idtype: int, name: str, type: str):
    """Create a card in the database."""
    with db_session:
        if not exists_card(id):
            Card(
                id=id,
                idtype=idtype,
                name=name,
                type=type,
            )
            commit()
        else:
            raise ValueError(f"Card with id {id} already exists.")


def add_available_deck_to_card(id: int, deck: AvailableDeck):
    """Add a deck to a card."""
    with db_session:
        if deck not in get_card(id).available_deck:
            get_card(id).available_deck.add(deck)
            commit()
        else:
            raise ValueError(
                f"Deck with id {deck.id} doesn't exists in card with id {id}."
            )


def add_disposable_deck_to_card(id: int, deck: DisposableDeck):
    """Add a deck to a card."""
    with db_session:
        if deck not in get_card(id).disposable_deck:
            get_card(id).disposable_deck.add(deck)
            commit()
        else:
            raise ValueError(
                f"Deck with id {deck.id} doesn't exists in card with id {id}."
            )


def add_player_to_card(id: int, player: Player):
    """Add a player to a card."""
    with db_session:
        if player not in get_card(id).players:
            get_card(id).players.add(player)
            commit()
        else:
            raise ValueError(
                f"Player with id {player.id} doesn't exists in card with id {id}."
            )


def remove_available_deck_from_card(id: int, deck: AvailableDeck):
    """Remove a deck from a card."""
    with db_session:
        if deck in get_card(id).available_deck:
            get_card(id).available_deck.remove(deck)
            commit()
        else:
            raise ValueError(
                f"Deck with id {deck.id} doesn't exists in card with id {id}."
            )


def remove_disposable_deck_from_card(id: int, deck: DisposableDeck):
    """Remove a deck from a card."""
    with db_session:
        if deck in get_card(id).disposable_deck:
            get_card(id).disposable_deck.remove(deck)
            commit()
        else:
            raise ValueError(
                f"Deck with id {deck.id} doesn't exists in card with id {id}."
            )


def remove_player_from_card(id: int, player: Player):
    """Remove a player from a card."""
    with db_session:
        if player in get_card(id).players:
            get_card(id).players.remove(player)
            commit()
        else:
            raise ValueError(
                f"Player with id {player.id} doesn't exists in card with id {id}."
            )
