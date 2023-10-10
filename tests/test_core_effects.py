"""Test card effects logic module."""
import pytest

from . import ActionType
from . import commit
from . import db_session
from . import Deck
from . import do_effect
from . import Game
from . import GameAction
from . import Player

# ============================ INVALID EFFECT ============================


class TestDoEffectInvalid:
    """Tests for invalid calls."""

    def init_db(self):
        """Init DB."""
        with db_session:
            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Game[1].delete()
            Deck[1].delete()
            commit()

    def test_invalid_card(self):
        """Test invalid card."""
        self.init_db()
        with pytest.raises(ValueError):
            do_effect(1, 0)

        with pytest.raises(ValueError):
            do_effect(1, 32)
        self.end_db()

    def test_invalid_game(self):
        """Test invalid game."""
        with pytest.raises(ValueError):
            do_effect(0, 1)

        with pytest.raises(ValueError):
            do_effect(2, 1)


# ============================ NOTHING EFFECT ============================


class TestDoEffectNothing:
    """Tests for nothing effects."""

    def init_db(self):
        """Init DB."""
        with db_session:
            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Game[1].delete()
            Deck[1].delete()
            commit()

    def test_nothing_effect(self):
        """Test nothing effect."""
        self.init_db()
        action = do_effect(1, 1)
        assert isinstance(action, GameAction)
        assert action.action == ActionType.NOTHING
        assert action.target is None
        self.end_db()

    def test_nothing_effect_with_invalid_phase(self):
        """Test nothing effect with invalid phase."""
        self.init_db()
        with db_session:
            Game[1].current_phase = "Draw"
            commit()

        with pytest.raises(ValueError):
            do_effect(1, 1)
        self.end_db()


# ============================ FLAMETHROWER EFFECT ============================


class TestDoEffectFlamethrower:
    """Tests for flamethrower effects."""

    def init_db(self):
        """Init DB."""
        with db_session:
            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            Player(id=1, name="Test", game=Game[1], round_position=1)
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Game[1].delete()
            Deck[1].delete()
            Player[1].delete()
            commit()

    def test_flamethrower_effect(self):
        """Test flamethrower effect."""
        self.init_db()
        action = do_effect(1, 3, 1)
        assert isinstance(action, GameAction)
        assert action.action == ActionType.KILL
        assert action.target == 1
        self.end_db()

    def test_flamethrower_effect_with_invalid_phase(self):
        """Test flamethrower effect with invalid phase."""
        self.init_db()
        with db_session:
            Game[1].current_phase = "Draw"
            commit()

        with pytest.raises(ValueError):
            do_effect(1, 3, 1)
        self.end_db()

    def test_flamethrower_effect_with_invalid_target(self):
        """Test flamethrower effect with invalid target."""
        self.init_db()
        with pytest.raises(ValueError):
            do_effect(1, 3, 2)

        with pytest.raises(ValueError):
            do_effect(1, 3, 3)

        with pytest.raises(ValueError):
            do_effect(1, 3, None)
        self.end_db()

    def test_flamethrower_effect_with_dead_target(self):
        """Test flamethrower effect with dead target."""
        self.init_db()
        with db_session:
            Player[1].alive = False
            commit()

        with pytest.raises(ValueError):
            do_effect(1, 3, 1)
        self.end_db()
