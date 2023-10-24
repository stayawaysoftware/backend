"""Test deck - database module."""
import pytest

from . import AvailableDeck
from . import Card
from . import clean_db
from . import commit
from . import create_available_deck
from . import create_deck
from . import create_disposable_deck
from . import db_session
from . import Deck
from . import delete_available_deck
from . import delete_deck
from . import delete_disposable_deck
from . import DisposableDeck
from . import exists_available_deck
from . import exists_deck
from . import exists_disposable_deck
from . import get_available_deck
from . import get_deck
from . import get_disposable_deck
from . import get_random_card_from_available_deck
from . import move_disposable_to_available_deck

# ===================== BASIC DECK FUNCTIONS =====================


class TestDeckBasic:
    """Test deck basic functions."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    @db_session
    def init_db(self):
        """Init DB."""
        Deck(id=1)
        AvailableDeck(id=1, deck=Deck[1])
        DisposableDeck(id=1, deck=Deck[1])
        commit()

    @db_session
    def end_db(self):
        """End DB."""
        Deck[1].delete()
        AvailableDeck[1].delete()
        DisposableDeck[1].delete()
        commit()

    # Exists

    def test_exists_deck(self):
        """Test exists_deck function."""
        self.init_db()
        assert exists_deck(1)
        self.end_db()

    def test_exists_deck_that_doesnt_exist(self):
        """Test exists_deck function with a deck that doesn't exist."""
        assert not exists_deck(1)

    def test_exists_available_deck(self):
        """Test exists_available_deck function."""
        self.init_db()
        assert exists_available_deck(1)
        self.end_db()

    def test_exists_available_deck_that_doesnt_exist(self):
        """Test exists_available_deck function with a deck that doesn't exist."""
        assert not exists_available_deck(1)

    def test_exists_disposable_deck(self):
        """Test exists_disposable_deck function."""
        self.init_db()
        assert exists_disposable_deck(1)
        self.end_db()

    def test_exists_disposable_deck_that_doesnt_exist(self):
        """Test exists_disposable_deck function with a deck that doesn't exist."""
        assert not exists_disposable_deck(1)

    # Get

    @db_session
    def test_get_deck(self):
        """Test get_deck function."""
        self.init_db()
        deck = get_deck(1)
        assert deck.id == 1
        assert deck.available_deck.id == 1
        self.end_db()

    @db_session
    def test_get_deck_that_doesnt_exist(self):
        """Test get_deck function with a deck that doesn't exist."""
        with pytest.raises(ValueError):
            get_deck(1)

    @db_session
    def test_get_available_deck(self):
        """Test get_available_deck function."""
        self.init_db()
        available_deck = get_available_deck(1)
        assert available_deck.id == 1
        assert available_deck.deck.id == 1
        self.end_db()

    @db_session
    def test_get_available_deck_that_doesnt_exist(self):
        """Test get_available_deck function with a deck that doesn't exist."""
        with pytest.raises(ValueError):
            get_available_deck(1)

    @db_session
    def test_get_disposable_deck(self):
        """Test get_disposable_deck function."""
        self.init_db()
        disposable_deck = get_disposable_deck(1)
        assert disposable_deck.id == 1
        assert disposable_deck.deck.id == 1
        self.end_db()

    @db_session
    def test_get_disposable_deck_that_doesnt_exist(self):
        """Test get_disposable_deck function with a deck that doesn't exist."""
        with pytest.raises(ValueError):
            get_disposable_deck(1)

    # Create

    @db_session
    def test_create_deck(self):
        """Test create_deck function."""
        deck = create_deck(1)
        assert deck.id == 1
        Deck[1].delete()

    @db_session
    def test_create_deck_that_already_exists(self):
        """Test create_deck function with a deck that already exists."""
        create_deck(1)
        with pytest.raises(ValueError):
            create_deck(1)
        Deck[1].delete()

    @db_session
    def test_create_available_deck(self):
        """Test create_available_deck function."""
        Deck(id=1)
        available_deck = create_available_deck(1)
        assert available_deck.id == 1
        assert available_deck.deck.id == 1
        AvailableDeck[1].delete()
        Deck[1].delete()

    @db_session
    def test_create_available_deck_that_already_exists(self):
        """Test create_available_deck function with a deck that already exists."""
        Deck(id=1)
        create_available_deck(1)
        with pytest.raises(ValueError):
            create_available_deck(1)
        AvailableDeck[1].delete()
        Deck[1].delete()

    @db_session
    def test_create_disposable_deck(self):
        """Test create_disposable_deck function."""
        Deck(id=1)
        disposable_deck = create_disposable_deck(1)
        assert disposable_deck.id == 1
        assert disposable_deck.deck.id == 1
        DisposableDeck[1].delete()
        Deck[1].delete()

    @db_session
    def test_create_disposable_deck_that_already_exists(self):
        """Test create_disposable_deck function with a deck that already exists."""
        Deck(id=1)
        create_disposable_deck(1)
        with pytest.raises(ValueError):
            create_disposable_deck(1)
        DisposableDeck[1].delete()
        Deck[1].delete()


# ===================== DECK - CARD FUNCTIONS =====================


class TestDeckCard:
    """Test deck - card functions."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    @db_session
    def init_db(self):
        """Init DB."""
        Deck(id=1)
        AvailableDeck(id=1, deck=Deck[1])
        DisposableDeck(id=1, deck=Deck[1])
        for i in range(1, 11):
            Card(id=i, idtype=i, name=f"Card {i}")
        commit()

    @db_session
    def end_db(self):
        """End DB."""
        Deck[1].delete()
        AvailableDeck[1].delete()
        DisposableDeck[1].delete()
        for i in range(1, 11):
            Card[i].delete()
        commit()

    # Get random card from available deck

    @db_session
    def test_get_random_card_from_available_deck(self):
        """Test get_random_card_from_available_deck function."""
        self.init_db()
        for i in range(1, 11):
            AvailableDeck[1].cards.add(Card[i])
        commit()

        card = get_random_card_from_available_deck(1)

        assert card.id in range(1, 11)
        self.end_db()

    @db_session
    def test_get_random_card_from_available_deck_that_is_empty(self):
        """Test get_random_card_from_available_deck function with an empty deck."""
        self.init_db()
        with pytest.raises(ValueError):
            get_random_card_from_available_deck(1)
        self.end_db()

    # Move cards

    @db_session
    def test_move_disposable_to_available_deck(self):
        """Test move_disposable_to_available_deck function."""
        self.init_db()
        for i in range(1, 11):
            DisposableDeck[1].cards.add(Card[i])
        commit()

        move_disposable_to_available_deck(1)

        assert len(DisposableDeck[1].cards) == 0
        assert len(AvailableDeck[1].cards) == 10
        self.end_db()

    @db_session
    def test_move_disposable_to_available_deck_with_disposable_empty(self):
        """Test move_disposable_to_available_deck function with an empty disposable deck."""
        self.init_db()
        with pytest.raises(ValueError):
            move_disposable_to_available_deck(1)
        self.end_db()

    @db_session
    def test_move_disposable_to_available_deck_with_available_not_empty(self):
        """Test move_disposable_to_available_deck function with a non-empty available deck."""
        self.init_db()
        AvailableDeck[1].cards.add(Card[1])
        for i in range(2, 11):
            DisposableDeck[1].cards.add(Card[i])
        commit()

        with pytest.raises(ValueError):
            move_disposable_to_available_deck(1)

        self.end_db()


# ===================== DELETE DECK FUNCTIONS =====================


class TestDeckDelete:
    """Test deck delete functions."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    @db_session
    def test_delete_deck(self):
        """Test delete_deck function."""
        Deck(id=1)
        delete_deck(1)
        assert not exists_deck(1)
        if Deck.exists():  # Only if the assert fails
            Deck[1].delete()

    @db_session
    def test_delete_deck_that_doesnt_exist(self):
        """Test delete_deck function with a deck that doesn't exist."""
        with pytest.raises(ValueError):
            delete_deck(1)

    @db_session
    def test_delete_available_deck(self):
        """Test delete_available_deck function."""
        Deck(id=1)
        AvailableDeck(id=1, deck=Deck[1])
        delete_available_deck(1)
        assert not exists_available_deck(1)
        if AvailableDeck.exists():  # Only if the assert fails
            AvailableDeck[1].delete()
        Deck[1].delete()

    @db_session
    def test_delete_available_deck_that_doesnt_exist(self):
        """Test delete_available_deck function with a deck that doesn't exist."""
        with pytest.raises(ValueError):
            delete_available_deck(1)

    @db_session
    def test_delete_disposable_deck(self):
        """Test delete_disposable_deck function."""
        Deck(id=1)
        DisposableDeck(id=1, deck=Deck[1])
        delete_disposable_deck(1)
        assert not exists_disposable_deck(1)
        if DisposableDeck.exists():  # Only if the assert fails
            DisposableDeck[1].delete()
        Deck[1].delete()

    @db_session
    def test_delete_disposable_deck_that_doesnt_exist(self):
        """Test delete_disposable_deck function with a deck that doesn't exist."""
        with pytest.raises(ValueError):
            delete_disposable_deck(1)
