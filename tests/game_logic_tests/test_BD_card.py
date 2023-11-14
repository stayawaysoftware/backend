"""Test card - database module."""
import pytest

from . import AvailableDeck
from . import Card
from . import clean_db
from . import commit
from . import create_card
from . import db_session
from . import Deck
from . import DisposableDeck
from . import exists_card
from . import Game
from . import get_card
from . import Player
from . import relate_card_with_available_deck
from . import relate_card_with_disposable_deck
from . import relate_card_with_player
from . import unrelate_card_with_available_deck
from . import unrelate_card_with_disposable_deck
from . import unrelate_card_with_player

# ===================== BASIC CARD FUNCTIONS =====================


class TestCardBasic:
    """Test basic card database functions."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def init_db(self):
        """Init DB."""
        with db_session:
            Card(id=1, idtype=1, name="Test card 1")
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Card[1].delete()
            commit()

    # Exists card

    def test_exists_card(self):
        """Test exists_card."""
        self.init_db()
        assert exists_card(1)
        self.end_db()

    def test_exists_card_with_invalid_id(self):
        """Test exists_card with invalid id."""
        assert not exists_card(1)

    # Get card

    def test_get_card(self):
        """Test get_card."""
        self.init_db()
        card = get_card(1)
        assert card.id == 1
        assert card.idtype == 1
        assert card.name == "Test card 1"
        assert card.type == "Action"
        self.end_db()

    def test_get_card_with_invalid_id(self):
        """Test get_card with invalid id."""
        with pytest.raises(ValueError):
            get_card(1)

    # Create card

    def test_create_card(self):
        """Test create_card."""
        card = create_card(2, 1, "Test card 2", "Action")
        assert card.id == 2
        assert card.idtype == 1
        assert card.name == "Test card 2"
        assert card.type == "Action"
        with db_session:
            Card[2].delete()
            commit()

    def test_create_card_that_already_exists(self):
        """Test create_card that already exists."""
        self.init_db()
        with pytest.raises(ValueError):
            create_card(1, 1, "Test card 1", "Action")
        self.end_db()


# ===================== RELATIONSHIP CARD FUNCTIONS =====================


class TestCardRelationship:
    """Test relationship card database functions."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def init_db(self):
        """Init DB."""
        with db_session:
            Card(id=1, idtype=1, name="Test card 1")
            Card(id=2, idtype=1, name="Test card 2")
            Card(id=3, idtype=2, name="Test card 3")

            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            AvailableDeck(id=1, deck=Deck[1])
            DisposableDeck(id=1, deck=Deck[1])

            Player(id=1, name="Test player 1", round_position=1, game=Game[1])
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Card[1].delete()
            Card[2].delete()
            Card[3].delete()

            Game[1].delete()
            Deck[1].delete()
            AvailableDeck[1].delete()
            DisposableDeck[1].delete()

            Player[1].delete()
            commit()

    # Relate card with available deck

    def test_relate_card_with_available_deck(self):
        """Test relate_card_with_available_deck."""
        self.init_db()
        relate_card_with_available_deck(1, 1)
        with db_session:
            assert AvailableDeck[1] in Card[1].available_deck
        self.end_db()

    def test_relate_card_with_available_deck_with_invalid_available_deck(self):
        """Test relate_card_with_available_deck with invalid available deck."""
        self.init_db()
        with pytest.raises(ValueError):
            relate_card_with_available_deck(1, 2)
        self.end_db()

    def test_relate_card_with_available_deck_already_related(self):
        """Test relate_card_with_available_deck already related."""
        self.init_db()
        relate_card_with_available_deck(1, 1)
        with pytest.raises(ValueError):
            relate_card_with_available_deck(1, 1)
        self.end_db()

    # Relate card with disposable deck

    def test_relate_card_with_disposable_deck(self):
        """Test relate_card_with_disposable_deck."""
        self.init_db()
        relate_card_with_disposable_deck(1, 1)
        with db_session:
            assert DisposableDeck[1] in Card[1].disposable_deck
        self.end_db()

    def test_relate_card_with_disposable_deck_with_invalid_disposable_deck(
        self,
    ):
        """Test relate_card_with_disposable_deck with invalid disposable deck."""
        self.init_db()
        with pytest.raises(ValueError):
            relate_card_with_disposable_deck(1, 2)
        self.end_db()

    def test_relate_card_with_disposable_deck_already_related(self):
        """Test relate_card_with_disposable_deck already related."""
        self.init_db()
        relate_card_with_disposable_deck(1, 1)
        with pytest.raises(ValueError):
            relate_card_with_disposable_deck(1, 1)
        self.end_db()

    # Relate card with player

    def test_relate_card_with_player(self):
        """Test relate_card_with_player."""
        self.init_db()
        relate_card_with_player(1, 1)
        with db_session:
            assert Player[1] in Card[1].players
        self.end_db()

    def test_relate_card_with_player_with_invalid_player(self):
        """Test relate_card_with_player with invalid player."""
        self.init_db()
        with pytest.raises(ValueError):
            relate_card_with_player(1, 2)
        self.end_db()

    def test_relate_card_with_player_already_related(self):
        """Test relate_card_with_player already related."""
        self.init_db()
        relate_card_with_player(1, 1)
        with pytest.raises(ValueError):
            relate_card_with_player(1, 1)
        self.end_db()


# ===================== UNRELATIONSHIP CARD FUNCTIONS =====================


class TestCardUnrelationship:
    """Test unrelationship card database functions."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def init_db(self):
        """Init DB."""
        with db_session:
            Card(id=1, idtype=1, name="Test card 1")
            Card(id=2, idtype=1, name="Test card 2")
            Card(id=3, idtype=2, name="Test card 3")

            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            AvailableDeck(id=1, deck=Deck[1])
            DisposableDeck(id=1, deck=Deck[1])

            Player(id=1, name="Test player 1", round_position=1, game=Game[1])
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Card[1].delete()
            Card[2].delete()
            Card[3].delete()

            Game[1].delete()
            Deck[1].delete()
            AvailableDeck[1].delete()
            DisposableDeck[1].delete()

            Player[1].delete()
            commit()

    # Unrelate card with available deck

    def test_unrelate_card_with_available_deck(self):
        """Test unrelate_card_with_available_deck."""
        self.init_db()
        with db_session:
            Card[1].available_deck.add(AvailableDeck[1])
            commit()
            assert AvailableDeck[1] in Card[1].available_deck

        unrelate_card_with_available_deck(1, 1)

        with db_session:
            assert AvailableDeck[1] not in Card[1].available_deck
        self.end_db()

    def test_unrelate_card_with_available_deck_with_invalid_available_deck(
        self,
    ):
        """Test unrelate_card_with_available_deck with invalid available deck."""
        self.init_db()
        with pytest.raises(ValueError):
            unrelate_card_with_available_deck(1, 2)
        self.end_db()

    def test_unrelate_card_with_available_deck_not_related(self):
        """Test unrelate_card_with_available_deck not related."""
        self.init_db()
        with pytest.raises(ValueError):
            unrelate_card_with_available_deck(1, 1)
        self.end_db()

    # Unrelate card with disposable deck

    def test_unrelate_card_with_disposable_deck(self):
        """Test unrelate_card_with_disposable_deck."""
        self.init_db()
        with db_session:
            Card[1].disposable_deck.add(DisposableDeck[1])
            commit()
            assert DisposableDeck[1] in Card[1].disposable_deck

        unrelate_card_with_disposable_deck(1, 1)

        with db_session:
            assert DisposableDeck[1] not in Card[1].disposable_deck
        self.end_db()

    def test_unrelate_card_with_disposable_deck_with_invalid_disposable_deck(
        self,
    ):
        """Test unrelate_card_with_disposable_deck with invalid disposable deck."""
        self.init_db()
        with pytest.raises(ValueError):
            unrelate_card_with_disposable_deck(1, 2)
        self.end_db()

    def test_unrelate_card_with_disposable_deck_not_related(self):
        """Test unrelate_card_with_disposable_deck not related."""
        self.init_db()
        with pytest.raises(ValueError):
            unrelate_card_with_disposable_deck(1, 1)
        self.end_db()

    # Unrelate card with player

    def test_unrelate_card_with_player(self):
        """Test unrelate_card_with_player."""
        self.init_db()
        with db_session:
            Card[1].players.add(Player[1])
            commit()
            assert Player[1] in Card[1].players

        unrelate_card_with_player(1, 1)

        with db_session:
            assert Player[1] not in Card[1].players
        self.end_db()

    def test_unrelate_card_with_player_with_invalid_player(self):
        """Test unrelate_card_with_player with invalid player."""
        self.init_db()
        with pytest.raises(ValueError):
            unrelate_card_with_player(1, 2)
        self.end_db()

    def test_unrelate_card_with_player_not_related(self):
        """Test unrelate_card_with_player not related."""
        self.init_db()
        with pytest.raises(ValueError):
            unrelate_card_with_player(1, 1)
        self.end_db()
