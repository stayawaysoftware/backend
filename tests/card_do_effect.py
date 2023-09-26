"""Test card do_effect method."""

import unittest

from src.core.game.card.card import Card
from src.core.game.game_action import GameAction

class SimpleTest(unittest.TestCase):
    """Simple test."""
    def test_do_effect1(self):
        """Test do_effect method 1."""
        card = Card(1, "Card 1", "Description 1", "Category 1", lambda game: GameAction("Action 1"))
        self.assertEqual(str(card.do_effect(None)), str(GameAction("Action 1")))

    def test_do_effect2(self):
        """Test do_effect method 2."""
        card = Card(2, "Card 2", "Description 2", "Category 2", lambda game: GameAction("Action 2", 1))
        self.assertEqual(str(card.do_effect(None)), str(GameAction("Action 2", 1)))

if __name__ == '__main__':
    unittest.main()
