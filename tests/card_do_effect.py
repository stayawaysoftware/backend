"""Test card do_effect method."""
import unittest
from src.core.game.card.card import Card
from src.core.game.card.effects import flamethrower_effect
from src.core.game.game import Game
from src.core.game.game_action import GameAction


class TestGameActionCreation(unittest.TestCase):
    """Test for Game Action creation."""

    def test_creation1(self):
        """Test do_effect method 1."""
        card = Card(
            1,
            "Card 1",
            "Description 1",
            "Category 1",
            lambda game, x: GameAction("Action 1", None),
        )
        self.assertEqual(
            str(card.do_effect(None, None)), str(GameAction("Action 1", None))
        )

    def test_creation2(self):
        """Test do_effect method 2."""
        card = Card(
            2,
            "Card 2",
            "Description 2",
            "Category 2",
            lambda game, x: GameAction("Action 2", x),
        )
        self.assertEqual(
            str(card.do_effect(None, 2)), str(GameAction("Action 2", 2))
        )

    def test_creation3(self):
        """Test do_effect method 3."""
        card = Card(
            3,
            "Card 3",
            "Description 3",
            "Category 3",
            lambda game, x: GameAction("Action 3", x),
        )
        self.assertEqual(
            str(card.do_effect(None, None)), str(GameAction("Action 3", None))
        )


class TestFlamethrowerEffect(unittest.TestCase):
    """Test for flamethrower_effect method."""

    def test_effect(self):
        """Test flamethrower_effect method."""
        card = Card(
            1, "Flamethrower", "Kill a player.", "ACTION", flamethrower_effect
        )
        game = Game(1, "Game 1", [1, 2, 3], 3, True, "PLAY", 1)
        self.assertEqual(
            str(card.do_effect(game, 2)), str(GameAction("KILL", 2))
        )

    def test_assert1(self):
        """Test flamethrower_effect method assertion 1 -> act_player = target."""
        card = Card(
            1, "Flamethrower", "Kill a player.", "ACTION", flamethrower_effect
        )
        game = Game(1, "Game 1", [1, 2, 3], 3, True, "PLAY", 1)
        self.assertRaises(AssertionError, card.do_effect, game, 1)

    def test_assert2(self):
        """Test flamethrower_effect method assertion 2 -> cnt_player = 1."""
        card = Card(
            1, "Flamethrower", "Kill a player.", "ACTION", flamethrower_effect
        )
        game = Game(1, "Game 1", [1], 1, True, "PLAY", 1)
        self.assertRaises(AssertionError, card.do_effect, game, 2)

    def test_assert3(self):
        """Test flamethrower_effect method assertion 3 -> act_phase != PLAY."""
        card = Card(
            1, "Flamethrower", "Kill a player.", "ACTION", flamethrower_effect
        )
        game = Game(1, "Game 1", [1, 2, 3], 3, True, "DRAW", 1)
        self.assertRaises(AssertionError, card.do_effect, game, 2)

    def test_assert4(self):
        """Test flamethrower_effect method assertion 4 -> target is None."""
        card = Card(
            1, "Flamethrower", "Kill a player.", "ACTION", flamethrower_effect
        )
        game = Game(1, "Game 1", [1, 2, 3], 3, True, "PLAY", 2)
        self.assertRaises(AssertionError, card.do_effect, game, None)


if __name__ == "__main__":
    unittest.main()
