"""Test game_action module."""
from . import ActionType
from . import GameAction


class TestGameAction:
    """Test game_action module."""

    def test_init(self):
        """Test initialization."""
        action = GameAction(ActionType.NOTHING)
        assert action.get_action() == ActionType.NOTHING
        assert action.get_target() is None

        action = GameAction(ActionType.KILL, 1)
        assert action.get_action() == ActionType.KILL
        assert action.get_target() == 1

    def test_str(self):
        """Test string representation."""
        action = GameAction(ActionType.NOTHING)
        assert str(action) == "Nothing"

        action = GameAction(ActionType.KILL, 1)
        assert str(action) == "Kill - 1"

    def test_get_action(self):
        """Test get_action()."""
        action = GameAction(ActionType.NOTHING)
        assert action.get_action() == ActionType.NOTHING

        action = GameAction(ActionType.KILL, 1)
        assert action.get_action() == ActionType.KILL

    def test_get_target(self):
        """Test get_target()."""
        action = GameAction(ActionType.NOTHING)
        assert action.get_target() is None

        action = GameAction(ActionType.KILL, 1)
        assert action.get_target() == 1

    def test_set_action(self):
        """Test set_action()."""
        action = GameAction(ActionType.NOTHING)
        action.set_action(ActionType.KILL)
        assert action.get_action() == ActionType.KILL

        action = GameAction(ActionType.KILL, 1)
        action.set_action(ActionType.NOTHING)
        assert action.get_action() == ActionType.NOTHING

    def test_set_target(self):
        """Test set_target()."""
        action = GameAction(ActionType.NOTHING)
        action.set_target(1)
        assert action.get_target() == 1

        action = GameAction(ActionType.KILL, 1)
        action.set_target(2)
        assert action.get_target() == 2
