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
            number=1,
            name="Card 1",
            description="Description 1",
            category="Category 1",
            effect=lambda game, x: GameAction("Action 1", None),
        )
        self.assertEqual(
            str(card.do_effect(game=None, target=None)),
            str(GameAction(action="Action 1", target=None)),
        )

    def test_creation2(self):
        """Test do_effect method 2."""
        card = Card(
            number=2,
            name="Card 2",
            description="Description 2",
            category="Category 2",
            effect=lambda game, x: GameAction("Action 2", x),
        )
        self.assertEqual(
            str(card.do_effect(game=None, target=2)),
            str(GameAction(action="Action 2", target=2)),
        )

    def test_creation3(self):
        """Test do_effect method 3."""
        card = Card(
            number=3,
            name="Card 3",
            description="Description 3",
            category="Category 3",
            effect=lambda game, x: GameAction("Action 3", x),
        )
        self.assertEqual(
            str(card.do_effect(game=None, target=None)),
            str(GameAction(action="Action 3", target=None)),
        )


class TestFlamethrowerEffect(unittest.TestCase):
    """Test for flamethrower_effect method."""

    def test_effect(self):
        """Test flamethrower_effect method."""
        card = Card(
            number=1,
            name="Flamethrower",
            description="Kill a player.",
            category="ACTION",
            effect=flamethrower_effect,
        )
        game = Game(
            game_id=1,
            name="Game 1",
            user_ids=[1, 2, 3],
            player_quantity=3,
            round_direction=True,
            actual_phase="PLAY",
            actual_turn=1,
        )
        self.assertEqual(
            str(card.do_effect(game=game, target=2)),
            str(GameAction(action="KILL", target=2)),
        )

    def test_assert1(self):
        """Test flamethrower_effect method assertion 1 -> act_player = target."""
        card = Card(
            number=1,
            name="Flamethrower",
            description="Kill a player.",
            category="ACTION",
            effect=flamethrower_effect,
        )
        game = Game(
            game_id=1,
            name="Game 1",
            user_ids=[1, 2, 3],
            player_quantity=3,
            round_direction=True,
            actual_phase="PLAY",
            actual_turn=1,
        )
        self.assertRaises(AssertionError, card.do_effect, game=game, target=1)

    def test_assert2(self):
        """Test flamethrower_effect method assertion 2 -> cnt_player = 1."""
        card = Card(
            number=1,
            name="Flamethrower",
            description="Kill a player.",
            category="ACTION",
            effect=flamethrower_effect,
        )
        game = Game(
            game_id=1,
            name="Game 1",
            user_ids=[1],
            player_quantity=1,
            round_direction=True,
            actual_phase="PLAY",
            actual_turn=1,
        )
        self.assertRaises(AssertionError, card.do_effect, game=game, target=2)

    def test_assert3(self):
        """Test flamethrower_effect method assertion 3 -> act_phase != PLAY."""
        card = Card(
            number=1,
            name="Flamethrower",
            description="Kill a player.",
            category="ACTION",
            effect=flamethrower_effect,
        )
        game = Game(
            game_id=1,
            name="Game 1",
            user_ids=[1, 2, 3],
            player_quantity=3,
            round_direction=True,
            actual_phase="DRAW",
            actual_turn=1,
        )
        self.assertRaises(AssertionError, card.do_effect, game=game, target=2)

    def test_assert4(self):
        """Test flamethrower_effect method assertion 4 -> target is None."""
        card = Card(
            number=1,
            name="Flamethrower",
            description="Kill a player.",
            category="ACTION",
            effect=flamethrower_effect,
        )
        game = Game(
            game_id=1,
            name="Game 1",
            user_ids=[1, 2, 3],
            player_quantity=3,
            round_direction=True,
            actual_phase="PLAY",
            actual_turn=2,
        )
        self.assertRaises(
            AssertionError, card.do_effect, game=game, target=None
        )


if __name__ == "__main__":
    unittest.main()
