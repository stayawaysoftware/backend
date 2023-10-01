"""Test game_action module."""
import os
import sys
import unittest

# Add src to path
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.append(src_dir)

from core.game_action import ActionType, GameAction


class TestGameAction(unittest.TestCase):
    """Test game_action module."""

    def test_init(self):
        """Test initialization."""
        action = GameAction(ActionType.NOTHING)
        self.assertEqual(action.get_action(), ActionType.NOTHING)
        self.assertEqual(action.get_target(), None)

        action = GameAction(ActionType.KILL, 1)
        self.assertEqual(action.get_action(), ActionType.KILL)
        self.assertEqual(action.get_target(), 1)

    def test_str(self):
        """Test string representation."""
        action = GameAction(ActionType.NOTHING)
        self.assertEqual(str(action), "Nothing")

        action = GameAction(ActionType.KILL, 1)
        self.assertEqual(str(action), "Kill - 1")

    def test_get_action(self):
        """Test get_action()."""
        action = GameAction(ActionType.NOTHING)
        self.assertEqual(action.get_action(), ActionType.NOTHING)

        action = GameAction(ActionType.KILL, 1)
        self.assertEqual(action.get_action(), ActionType.KILL)

    def test_get_target(self):
        """Test get_target()."""
        action = GameAction(ActionType.NOTHING)
        self.assertEqual(action.get_target(), None)

        action = GameAction(ActionType.KILL, 1)
        self.assertEqual(action.get_target(), 1)

    def test_set_action(self):
        """Test set_action()."""
        action = GameAction(ActionType.NOTHING)
        action.set_action(ActionType.KILL)
        self.assertEqual(action.get_action(), ActionType.KILL)

        action = GameAction(ActionType.KILL, 1)
        action.set_action(ActionType.NOTHING)
        self.assertEqual(action.get_action(), ActionType.NOTHING)

    def test_set_target(self):
        """Test set_target()."""
        action = GameAction(ActionType.NOTHING)
        action.set_target(1)
        self.assertEqual(action.get_target(), 1)

        action = GameAction(ActionType.KILL, 1)
        action.set_target(2)
        self.assertEqual(action.get_target(), 2)


if __name__ == "__main__":
    unittest.main()
