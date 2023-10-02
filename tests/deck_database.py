"""Test card database."""
import os
import sys
import unittest

# Add src to path
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.append(src_dir)

from core.deck import (
    exists_deck,
    exists_available_deck,
    exists_disposable_deck,
    get_deck,
    get_available_deck,
    get_disposable_deck,
    create_deck,
    create_available_deck,
    create_disposable_deck,
    add_card_to_available_deck,
    add_card_to_disposable_deck,
    remove_card_from_available_deck,
    remove_card_from_disposable_deck,
    remove_deck,
    remove_available_deck,
    remove_disposable_deck,
)
from models import db
from models.game import AvailableDeck
from models.game import Card
from models.game import Deck
from models.game import DisposableDeck
from models.game import Game
from pony.orm import commit
from pony.orm import db_session


class TestCardDatabase(unittest.TestCase):
    """Test card database."""

    @classmethod
    def setUpClass(cls):
        db.bind(provider="sqlite", filename=":memory:")
        db.generate_mapping(create_tables=True)

        with db_session:
            cls.game = Game(id=1)
            cls.card = Card(id=1, idtype=1, name="Test", type="Action")
            cls.deck = Deck(id=1)
            cls.available_deck = AvailableDeck(id=1, deck=cls.deck)
            cls.disposable_deck = DisposableDeck(id=1, deck=cls.deck)
            commit()

    @classmethod
    def tearDownClass(cls):
        db.drop_all_tables(with_all_data=True)

    def test_exists_deck(self):
        """Test exists_deck function."""
        self.assertTrue(exists_deck(1))
        self.assertFalse(exists_deck(2))

    def test_exists_available_deck(self):
        """Test exists_available_deck function."""
        self.assertTrue(exists_available_deck(1))
        self.assertFalse(exists_available_deck(2))

    def test_exists_disposable_deck(self):
        """Test exists_disposable_deck function."""
        self.assertTrue(exists_disposable_deck(1))
        self.assertFalse(exists_disposable_deck(2))

    def test_get_deck(self):
        """Test get_deck function."""
        with db_session:
            self.assertEqual(get_deck(1), Deck[1])
        with self.assertRaises(ValueError):
            get_deck(2)

    def test_get_available_deck(self):
        """Test get_available_deck function."""
        with db_session:
            self.assertEqual(get_available_deck(1), AvailableDeck[1])
        with self.assertRaises(ValueError):
            get_available_deck(2)

    def test_get_disposable_deck(self):
        """Test get_disposable_deck function."""
        with db_session:
            self.assertEqual(get_disposable_deck(1), DisposableDeck[1])
        with self.assertRaises(ValueError):
            get_disposable_deck(2)

    def test_create_deck(self):
        """Test create_deck function."""
        with db_session:
            create_deck(2)
            self.assertTrue(Deck.exists(id=2))

        with self.assertRaises(ValueError):
            create_deck(2)

        with db_session:
            Deck[2].delete()
            commit()

    def test_create_available_deck(self):
        """Test create_available_deck function."""
        with db_session:
            create_available_deck(2, Deck[1])
            self.assertTrue(AvailableDeck.exists(id=2))
            self.assertTrue(AvailableDeck.exists(deck=Deck[1]))

        with db_session, self.assertRaises(ValueError):
            create_available_deck(2, Deck[1])

        with db_session:
            AvailableDeck[2].delete()
            commit()

    def test_create_disposable_deck(self):
        """Test create_disposable_deck function."""
        with db_session:
            create_disposable_deck(2, Deck[1])
            self.assertTrue(DisposableDeck.exists(id=2))
            self.assertTrue(DisposableDeck.exists(deck=Deck[1]))

        with db_session, self.assertRaises(ValueError):
            create_disposable_deck(2, Deck[1])

        with db_session:
            DisposableDeck[2].delete()
            commit()

    def test_add_card_to_available_deck(self):
        """Test add_card_to_available_deck function."""
        with db_session:
            add_card_to_available_deck(1, Card[1])
            self.assertTrue(Card[1] in AvailableDeck[1].cards)

        with db_session, self.assertRaises(ValueError):
            add_card_to_available_deck(1, Card[1])

        with db_session:
            AvailableDeck[1].cards.remove(Card[1])
            commit()

    def test_add_card_to_disposable_deck(self):
        """Test add_card_to_disposable_deck function."""
        with db_session:
            add_card_to_disposable_deck(1, Card[1])
            self.assertTrue(Card[1] in DisposableDeck[1].cards)

        with db_session, self.assertRaises(ValueError):
            add_card_to_disposable_deck(1, Card[1])

        with db_session:
            DisposableDeck[1].cards.remove(Card[1])
            commit()

    def test_remove_card_from_available_deck(self):
        """Test remove_card_from_available_deck function."""
        with db_session:
            AvailableDeck[1].cards.add(Card[1])
            remove_card_from_available_deck(1, Card[1])
            self.assertTrue(Card[1] not in AvailableDeck[1].cards)

        with db_session, self.assertRaises(ValueError):
            remove_card_from_available_deck(1, Card[1])

    def test_remove_card_from_disposable_deck(self):
        """Test remove_card_from_disposable_deck function."""
        with db_session:
            DisposableDeck[1].cards.add(Card[1])
            remove_card_from_disposable_deck(1, Card[1])
            self.assertTrue(Card[1] not in DisposableDeck[1].cards)

        with db_session, self.assertRaises(ValueError):
            remove_card_from_disposable_deck(1, Card[1])

    def test_remove_deck(self):
        """Test remove_deck function."""
        with db_session:
            Deck(id=2)
            remove_deck(2)
            self.assertFalse(Deck.exists(id=2))

        with db_session, self.assertRaises(ValueError):
            remove_deck(2)

    def test_remove_available_deck(self):
        """Test remove_available_deck function."""
        with db_session:
            AvailableDeck(id=2, deck=Deck[1])
            remove_available_deck(2)
            self.assertFalse(AvailableDeck.exists(id=2))

        with db_session, self.assertRaises(ValueError):
            remove_available_deck(2)

    def test_remove_disposable_deck(self):
        """Test remove_disposable_deck function."""
        with db_session:
            DisposableDeck(id=2, deck=Deck[1])
            remove_disposable_deck(2)
            self.assertFalse(DisposableDeck.exists(id=2))

        with db_session, self.assertRaises(ValueError):
            remove_disposable_deck(2)


if __name__ == "__main__":
    unittest.main()
