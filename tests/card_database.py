"""Test card database."""
import os
import sys
import unittest

# Add src to path
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.append(src_dir)

from core.card import add_available_deck_to_card
from core.card import add_disposable_deck_to_card
from core.card import add_player_to_card
from core.card import create_card
from core.card import exists_card
from core.card import get_card
from core.card import remove_available_deck_from_card
from core.card import remove_disposable_deck_from_card
from core.card import remove_player_from_card
from models import db
from models.game import AvailableDeck
from models.game import Card
from models.game import Deck
from models.game import DisposableDeck
from models.game import Game
from models.game import Player
from pony.orm import commit
from pony.orm import db_session


class TestCardDatabase(unittest.TestCase):
    """Test card database."""

    @classmethod
    def setUpClass(cls):
        db.bind(provider="sqlite", filename=":memory:")
        db.generate_mapping(create_tables=True)
        create_card(1, 1, "Card 1", "Action")
        create_card(2, 2, "Card 2", "Defense")
        create_card(3, 3, "Card 3", "Infection")
        commit()

    @classmethod
    def tearDownClass(cls):
        db.drop_all_tables(with_all_data=True)

    def test_exists_card(self):
        """Test exists_card function."""
        self.assertTrue(exists_card(1))
        self.assertTrue(exists_card(2))
        self.assertTrue(exists_card(3))
        self.assertFalse(exists_card(4))
        self.assertFalse(exists_card(5))

    def test_get_card(self):
        """Test get_card function."""
        self.assertEqual(get_card(1).name, "Card 1")
        self.assertEqual(get_card(2).name, "Card 2")
        self.assertEqual(get_card(3).name, "Card 3")
        with self.assertRaises(ValueError):
            get_card(4)
        with self.assertRaises(ValueError):
            get_card(5)

    def test_create_card(self):
        """Test create_card function."""
        try:
            with db_session:
                create_card(4, 4, "Card 4", "Obstacle")
                commit()

                self.assertTrue(exists_card(4))
                self.assertEqual(get_card(4).idtype, 4)
                self.assertEqual(get_card(4).name, "Card 4")
                self.assertEqual(get_card(4).type, "Obstacle")

                Card.get(id=4).delete()
                commit()
        except ValueError:
            self.fail("create_card raised ValueError unexpectedly!")

    def test_create_card_already_exists(self):
        """Test create_card function when card already exists."""
        with self.assertRaises(ValueError):
            create_card(1, 1, "Card 1", "Action")
        with self.assertRaises(ValueError):
            create_card(2, 3, "Card 2", "Defense")
        with self.assertRaises(ValueError):
            create_card(3, 5, "Card 3", "Infection")

    def test_add_deck_to_card(self):
        """Test add_deck_to_card function."""
        try:
            with db_session:
                test_deck = Deck(id=1)
                test_available_deck = AvailableDeck(id=2, deck=test_deck)
                test_disposable_deck = DisposableDeck(id=3, deck=test_deck)
                commit()

                add_available_deck_to_card(1, test_available_deck)
                add_disposable_deck_to_card(1, test_disposable_deck)

                self.assertEqual(
                    get_card(1).available_deck.select().first(),
                    test_available_deck,
                )
                self.assertEqual(
                    get_card(1).disposable_deck.select().first(),
                    test_disposable_deck,
                )

                DisposableDeck.get(id=3).delete()
                AvailableDeck.get(id=2).delete()
                Deck.get(id=1).delete()
                commit()
        except ValueError:
            self.fail("add_deck_to_card raised ValueError unexpectedly!")

    def test_add_deck_to_card_deck_doesnt_exists(self):
        """Test add_deck_to_card function when deck doesn't exists."""
        with self.assertRaises(ValueError):
            add_available_deck_to_card(1, AvailableDeck(id=2))
        with self.assertRaises(ValueError):
            add_disposable_deck_to_card(1, DisposableDeck(id=3))

    def test_add_deck_to_card_card_doesnt_exists(self):
        """Test add_deck_to_card function when card doesn't exists."""
        with self.assertRaises(ValueError):
            add_available_deck_to_card(4, AvailableDeck(id=2))
        with self.assertRaises(ValueError):
            add_disposable_deck_to_card(4, DisposableDeck(id=3))

    def test_add_deck_to_card_deck_already_added(self):
        """Test add_deck_to_card function when deck already added."""
        with db_session:
            test_deck = Deck(id=1)
            test_available_deck = AvailableDeck(id=2, deck=test_deck)
            test_disposable_deck = DisposableDeck(id=3, deck=test_deck)
            commit()

            add_available_deck_to_card(1, test_available_deck)
            add_disposable_deck_to_card(1, test_disposable_deck)

            with self.assertRaises(ValueError):
                add_available_deck_to_card(1, test_available_deck)
            with self.assertRaises(ValueError):
                add_disposable_deck_to_card(1, test_disposable_deck)

            DisposableDeck.get(id=3).delete()
            AvailableDeck.get(id=2).delete()
            Deck.get(id=1).delete()
            commit()

    def test_add_player_to_card(self):
        """Test add_player_to_card function."""
        try:
            with db_session:
                test_deck = Deck(id=1)
                test_game = Game(id=1, deck=test_deck)
                test_player = Player(id=1, round_position=1, game=test_game)
                commit()

                add_player_to_card(1, test_player)

                self.assertEqual(
                    get_card(1).players.select().first(), test_player
                )

                Player.get(id=1).delete()
                Game.get(id=1).delete()
                Deck.get(id=1).delete()
                commit()
        except ValueError:
            self.fail("add_player_to_card raised ValueError unexpectedly!")

    def test_add_player_to_card_player_doesnt_exists(self):
        """Test add_player_to_card function when player doesn't exists."""
        with self.assertRaises(ValueError):
            add_player_to_card(1, Player(id=1))

    def test_add_player_to_card_card_doesnt_exists(self):
        """Test add_player_to_card function when card doesn't exists."""
        with self.assertRaises(ValueError):
            add_player_to_card(4, Player(id=1))

    def test_add_player_to_card_player_already_added(self):
        """Test add_player_to_card function when player already added."""
        with db_session:
            test_deck = Deck(id=1)
            test_game = Game(id=1, deck=test_deck)
            test_player = Player(id=1, round_position=1, game=test_game)
            commit()

            add_player_to_card(1, test_player)

            with self.assertRaises(ValueError):
                add_player_to_card(1, test_player)

            Player.get(id=1).delete()
            Game.get(id=1).delete()
            Deck.get(id=1).delete()
            commit()

    def test_remove_deck_from_card(self):
        """Test remove_deck_from_card function."""
        try:
            with db_session:
                test_deck = Deck(id=1)
                test_available_deck = AvailableDeck(id=2, deck=test_deck)
                test_disposable_deck = DisposableDeck(id=3, deck=test_deck)
                commit()

                add_available_deck_to_card(1, test_available_deck)
                add_disposable_deck_to_card(1, test_disposable_deck)

                remove_available_deck_from_card(1, test_available_deck)
                remove_disposable_deck_from_card(1, test_disposable_deck)

                self.assertEqual(
                    get_card(1).available_deck.select().first(), None
                )
                self.assertEqual(
                    get_card(1).disposable_deck.select().first(), None
                )

                DisposableDeck.get(id=3).delete()
                AvailableDeck.get(id=2).delete()
                Deck.get(id=1).delete()
                commit()
        except ValueError:
            self.fail("remove_deck_from_card raised ValueError unexpectedly!")

    def test_remove_deck_from_card_deck_doesnt_exists(self):
        """Test remove_deck_from_card function when deck doesn't exists."""
        with self.assertRaises(ValueError):
            remove_available_deck_from_card(1, AvailableDeck(id=2))
        with self.assertRaises(ValueError):
            remove_disposable_deck_from_card(1, DisposableDeck(id=3))

    def test_remove_deck_from_card_card_doesnt_exists(self):
        """Test remove_deck_from_card function when card doesn't exists."""
        with self.assertRaises(ValueError):
            remove_available_deck_from_card(4, AvailableDeck(id=2))
        with self.assertRaises(ValueError):
            remove_disposable_deck_from_card(4, DisposableDeck(id=3))

    def test_remove_deck_from_card_deck_already_removed(self):
        """Test remove_deck_from_card function when deck already removed."""
        with db_session:
            test_deck = Deck(id=1)
            test_available_deck = AvailableDeck(id=2, deck=test_deck)
            test_disposable_deck = DisposableDeck(id=3, deck=test_deck)
            commit()

            add_available_deck_to_card(1, test_available_deck)
            add_disposable_deck_to_card(1, test_disposable_deck)

            remove_available_deck_from_card(1, test_available_deck)
            remove_disposable_deck_from_card(1, test_disposable_deck)

            with self.assertRaises(ValueError):
                remove_available_deck_from_card(1, test_available_deck)
            with self.assertRaises(ValueError):
                remove_disposable_deck_from_card(1, test_disposable_deck)

            DisposableDeck.get(id=3).delete()
            AvailableDeck.get(id=2).delete()
            Deck.get(id=1).delete()
            commit()

    def test_remove_player_from_card(self):
        """Test remove_player_from_card function."""
        try:
            with db_session:
                test_deck = Deck(id=1)
                test_game = Game(id=1, deck=test_deck)
                test_player = Player(id=1, round_position=1, game=test_game)
                commit()

                add_player_to_card(1, test_player)

                remove_player_from_card(1, test_player)

                self.assertEqual(get_card(1).players.select().first(), None)

                Player.get(id=1).delete()
                Game.get(id=1).delete()
                Deck.get(id=1).delete()
                commit()
        except ValueError:
            self.fail(
                "remove_player_from_card raised ValueError unexpectedly!"
            )

    def test_remove_player_from_card_player_doesnt_exists(self):
        """Test remove_player_from_card function when player doesn't exists."""
        with self.assertRaises(ValueError):
            remove_player_from_card(1, Player(id=1))

    def test_remove_player_from_card_card_doesnt_exists(self):
        """Test remove_player_from_card function when card doesn't exists."""
        with self.assertRaises(ValueError):
            remove_player_from_card(4, Player(id=1))

    def test_remove_player_from_card_player_already_removed(self):
        """Test remove_player_from_card function when player already removed."""
        with db_session:
            test_deck = Deck(id=1)
            test_game = Game(id=1, deck=test_deck)
            test_player = Player(id=1, round_position=1, game=test_game)
            commit()

            add_player_to_card(1, test_player)

            remove_player_from_card(1, test_player)

            with self.assertRaises(ValueError):
                remove_player_from_card(1, test_player)

            Player.get(id=1).delete()
            Game.get(id=1).delete()
            Deck.get(id=1).delete()
            commit()


if __name__ == "__main__":
    unittest.main()
