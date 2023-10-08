"""Card database related functions."""
from models.game import AvailableDeck
from models.game import Card
from models.game import DisposableDeck
from models.game import Player
from pony.orm import commit
from pony.orm import db_session

# ===================== BASIC CARD FUNCTIONS =====================


def exists_card(id: int) -> bool:
    """Check if a card exists in the database"""
    with db_session:
        return Card.exists(id=id)


def get_card(id: int) -> Card:
    """Get a card from the database"""
    with db_session:
        if exists_card(id):
            return Card[id]
        raise ValueError(f"Card with id {id} doesn't exist")


def create_card(id: int, idtype: int, name: str, type: str) -> Card:
    """Create a card in the database"""
    with db_session:
        if not exists_card(id):
            card = Card(id=id, idtype=idtype, name=name, type=type)
            commit()
            return card
        raise ValueError(f"Card with id {id} already exists")


# ===================== RELATIONSHIP CARD FUNCTIONS =====================


def relate_card_with_available_deck(
    id_card: int, id_available_deck: int
) -> None:
    """Relate a card with an available deck"""
    with db_session:
        if not AvailableDeck.exists(id=id_available_deck):
            raise ValueError(
                f"Available deck with id {id_available_deck} doesn't exist"
            )

        available_deck = AvailableDeck[id_available_deck]
        card = get_card(id_card)

        if available_deck not in card.available_deck:
            card.available_deck.add(available_deck)
            commit()
        else:
            raise ValueError(
                f"Card with id {id_card} already related with available deck with id {id_available_deck}"
            )


def relate_card_with_disposable_deck(
    id_card: int, id_disposable_deck: int
) -> None:
    """Relate a card with a disposable deck"""
    with db_session:
        if not DisposableDeck.exists(id=id_disposable_deck):
            raise ValueError(
                f"Disposable deck with id {id_disposable_deck} doesn't exist"
            )

        disposable_deck = DisposableDeck[id_disposable_deck]
        card = get_card(id_card)

        if disposable_deck not in card.disposable_deck:
            card.disposable_deck.add(disposable_deck)
            commit()
        else:
            raise ValueError(
                f"Card with id {id_card} already related with disposable deck with id {id_disposable_deck}"
            )


def relate_card_with_player(id_card: int, id_player: int) -> None:
    """Relate a card with a player"""
    with db_session:
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")

        player = Player[id_player]
        card = get_card(id_card)

        if player not in card.players:
            card.players.add(player)
            commit()
        else:
            raise ValueError(
                f"Card with id {id_card} already related with player with id {id_player}"
            )


# ===================== UNRELATIONSHIP CARD FUNCTIONS =====================


def unrelate_card_with_available_deck(
    id_card: int, id_available_deck: int
) -> None:
    """Unrelate a card with an available deck"""
    with db_session:
        if not AvailableDeck.exists(id=id_available_deck):
            raise ValueError(
                f"Available deck with id {id_available_deck} doesn't exist"
            )

        available_deck = AvailableDeck[id_available_deck]
        card = get_card(id_card)

        if available_deck in card.available_deck:
            card.available_deck.remove(available_deck)
            commit()
        else:
            raise ValueError(
                f"Card with id {id_card} not related with available deck with id {id_available_deck}"
            )


def unrelate_card_with_disposable_deck(
    id_card: int, id_disposable_deck: int
) -> None:
    """Unrelate a card with a disposable deck"""
    with db_session:
        if not DisposableDeck.exists(id=id_disposable_deck):
            raise ValueError(
                f"Disposable deck with id {id_disposable_deck} doesn't exist"
            )

        disposable_deck = DisposableDeck[id_disposable_deck]
        card = get_card(id_card)

        if disposable_deck in card.disposable_deck:
            card.disposable_deck.remove(disposable_deck)
            commit()
        else:
            raise ValueError(
                f"Card with id {id_card} not related with disposable deck with id {id_disposable_deck}"
            )


def unrelate_card_with_player(id_card: int, id_player: int) -> None:
    """Unrelate a card with a player"""
    with db_session:
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")

        player = Player[id_player]
        card = get_card(id_card)

        if player in card.players:
            card.players.remove(player)
            commit()
        else:
            raise ValueError(
                f"Card with id {id_card} not related with player with id {id_player}"
            )
