"""Test functions used to all the game operation (internal logic)."""
from . import AvailableDeck
from . import Card
from . import commit
from . import db_session
from . import Deck
from . import DisposableDeck
from . import Game
from . import initialize_decks
from . import Player

# ===================== BASIC GAME FUNCTIONS =====================


class TestGameUtilityBasic:
    """Test basic game functions."""

    @db_session
    def init_db(self):
        """Init DB"""
        assert Game.select().count() == 0
        assert Player.select().count() == 0
        assert Deck.select().count() == 0
        assert AvailableDeck.select().count() == 0
        assert DisposableDeck.select().count() == 0
        assert Card.select().count() == 0

        Game(id=1)
        for i in range(1, 13):
            Player(id=i, name=f"Player{i}", round_position=i, game=Game[1])
        commit()

    @db_session
    def delete_db(self):
        """Delete DB"""
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()

    @db_session
    def test_initialize_decks(self):
        """Test initialize_decks function."""
        self.init_db()
        deck = initialize_decks(1, 12)

        assert Deck.exists(id=1)
        assert AvailableDeck.exists(id=1)
        assert DisposableDeck.exists(id=1)

        assert deck == Deck[1]

        assert deck.available_deck.id == 1
        assert deck.disposable_deck.id == 1
        assert AvailableDeck[1].deck.id == 1
        assert DisposableDeck[1].deck.id == 1

        assert len(AvailableDeck[1].cards) == 109

        AvailableDeck[1].delete()
        DisposableDeck[1].delete()
        Deck[1].delete()
        self.delete_db()


# ===================== GAME PHASES FUNCTIONS =====================

# DRAW phase

# PLAY phase

# DISCARD phase
