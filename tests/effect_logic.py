"""Test card effects logic module."""
import os
import sys
import unittest

# Add src to path
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.append(src_dir)

from core.game_action import ActionType, GameAction
from core.effects import do_effect

from models.game import Game, Player
from models import db
from pony.orm import db_session, commit


class TestDoEffect(unittest.TestCase):
    """Tests for do_effect function."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        db.bind(provider="sqlite", filename=":memory:")
        db.generate_mapping(create_tables=True)

        with db_session:
            game = Game(
                id=1,
                round_left_direction=0,
                actual_phase="Play",
                actual_position=1,
            )
            Player(id=1, game=game, round_position=1)
            commit()

    @classmethod
    def tearDownClass(cls):
        """Tear down test environment."""
        db.drop_all_tables(with_all_data=True)

    def test_invalid_card(self):
        """Test invalid card."""
        self.assertRaises(ValueError, do_effect, 1, 0)
        self.assertRaises(ValueError, do_effect, 1, 32)

    def test_invalid_game(self):
        """Test invalid game."""
        self.assertRaises(ValueError, do_effect, 0, 1)
        self.assertRaises(ValueError, do_effect, 2, 1)

    # Nothing effect
    def test_nothing_effect(self):
        """Test nothing effect."""
        action = do_effect(1, 1)
        self.assertIsInstance(action, GameAction)
        self.assertEqual(action.action, ActionType.NOTHING)
        self.assertIsNone(action.target)

    def test_nothing_effect_with_invalid_phase(self):
        """Test nothing effect with invalid phase."""
        with db_session:
            game = Game[1]
            game.actual_phase = "Draw"
            commit()

        self.assertRaises(ValueError, do_effect, 1, 1)

        with db_session:
            game = Game[1]
            game.actual_phase = "Play"
            commit()

    # Flamethrower effect
    def test_flamethrower_effect(self):
        """Test flamethrower effect."""
        action = do_effect(1, 3, 1)
        self.assertIsInstance(action, GameAction)
        self.assertEqual(action.action, ActionType.KILL)
        self.assertEqual(action.target, 1)

    def test_flamethrower_effect_with_invalid_phase(self):
        """Test flamethrower effect with invalid phase."""
        with db_session:
            game = Game[1]
            game.actual_phase = "Draw"
            commit()

        self.assertRaises(ValueError, do_effect, 1, 3, 1)

        with db_session:
            game = Game[1]
            game.actual_phase = "Play"
            commit()

    def test_flamethrower_effect_with_invalid_target(self):
        """Test flamethrower effect with invalid target."""
        self.assertRaises(ValueError, do_effect, 1, 3, 2)
        self.assertRaises(ValueError, do_effect, 1, 3, 3)
        self.assertRaises(ValueError, do_effect, 1, 3, None)

    def test_flamethrower_effect_with_dead_target(self):
        """Test flamethrower effect with dead target."""
        with db_session:
            player = Player[1]
            player.alive = False
            commit()

        self.assertRaises(ValueError, do_effect, 1, 3, 1)

        with db_session:
            player = Player[1]
            player.alive = True
            commit()


if __name__ == "__main__":
    unittest.main()
