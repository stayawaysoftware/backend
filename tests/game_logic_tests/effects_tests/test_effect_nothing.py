"""Test Nothing Effect."""
from . import ActionType
from . import clean_db
from . import db_session
from . import GameAction
from . import nothing_effect

# ============================ NOTHING EFFECT ============================


class TestNothingEffect:
    """Tests for nothing effect."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def test_nothing_effect(self):
        """Test nothing effect."""

        assert str(nothing_effect(1)) == str(
            GameAction(action=ActionType.NOTHING)
        )
