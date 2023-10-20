"""Test card effects logic module."""
import pytest

from . import ActionType
from . import clean_db
from . import commit
from . import db_session
from . import Deck
from . import do_effect
from . import Game
from . import GameAction
from . import nothing_effect
from . import Player
from . import without_defense_effect

# ============================ INVALID EFFECT ============================


class TestDoEffectInvalid:
    """Tests for invalid calls."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def init_db(self):
        """Init DB."""
        with db_session:
            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            Player(
                id=1,
                game=Game[1],
                alive=True,
                round_position=1,
                name="Player 1",
            )
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Game[1].delete()
            Deck[1].delete()
            Player[1].delete()
            commit()

    def test_invalid_id_card_type(self):
        """Test invalid id_card_type."""
        self.init_db()

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=100)

        self.end_db()

    def test_invalid_id_player(self):
        """Test invalid id_player."""
        self.init_db()

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=100, id_card_type=1)

        self.end_db()

    def test_invalid_id_game(self):
        """Test invalid id_game."""
        self.init_db()

        with pytest.raises(ValueError):
            do_effect(id_game=100, id_player=1, id_card_type=1)

        self.end_db()

    def test_invalid_card_to_play(self):
        """Test invalid card to play."""
        self.init_db()

        # The Thing
        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=1)

        # Infected
        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=2)

        self.end_db()


# ============================ WITHOUT DEFENSE EFFECT (ONLI INVALID THINGS) ============================


class TestWithoutDefenseEffectInvalid:
    """Tests for without defense effect (invalid things)."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def init_db(self):
        """Init DB."""
        with db_session:
            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            Player(
                id=1,
                game=Game[1],
                alive=True,
                round_position=1,
                name="Player 1",
            )
            Player(
                id=2,
                game=Game[1],
                alive=True,
                round_position=2,
                name="Player 2",
            )
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Game[1].delete()
            Deck[1].delete()
            Player[1].delete()
            Player[2].delete()
            commit()

    @db_session
    def test_without_defense_effect_in_wrong_phase(self):
        """Test without defense effect in wrong phase."""
        self.init_db()

        Game[1].current_phase = "Discard"
        with pytest.raises(ValueError):
            without_defense_effect(
                id_game=1,
                id_player=1,
                target=2,
                id_card_type_before=3,
                card_chosen_by_player=None,
                card_chosen_by_target=None,
            )

        self.end_db()

    @db_session
    def test_without_defense_effect_without_target(self):
        """Test without defense effect without target."""
        self.init_db()

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            without_defense_effect(
                id_game=1,
                id_player=1,
                id_card_type_before=3,
                target=None,
                card_chosen_by_player=None,
                card_chosen_by_target=None,
            )

        self.end_db()

    @db_session
    def test_without_defense_effect_with_invalid_target(self):
        """Test without defense effect with invalid target."""
        self.init_db()

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            without_defense_effect(
                id_game=1,
                id_player=1,
                id_card_type_before=3,
                target=100,
                card_chosen_by_player=None,
                card_chosen_by_target=None,
            )

        self.end_db()

    @db_session
    def test_without_defense_effect_with_dead_target(self):
        """Test without defense effect with dead target."""
        self.init_db()

        Player[2].alive = False

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            without_defense_effect(
                id_game=1,
                id_player=1,
                id_card_type_before=3,
                target=2,
                card_chosen_by_player=None,
                card_chosen_by_target=None,
            )

        self.end_db()

    @db_session
    def test_without_defense_effect_with_invalid_player(self):
        """Test without defense effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            without_defense_effect(
                id_game=1,
                id_player=100,
                id_card_type_before=3,
                target=2,
                card_chosen_by_player=None,
                card_chosen_by_target=None,
            )

        self.end_db()

    @db_session
    def test_without_defense_effect_with_player_as_target(self):
        """Test without defense effect with player as target."""
        self.init_db()

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            without_defense_effect(
                id_game=1,
                id_player=1,
                id_card_type_before=3,
                target=1,
                card_chosen_by_player=None,
                card_chosen_by_target=None,
            )

        self.end_db()

    @db_session
    def test_without_defense_effect_without_card_before(self):
        """Test without defense effect without card before."""
        self.init_db()

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            without_defense_effect(
                id_game=1,
                id_player=1,
                id_card_type_before=None,
                target=2,
                card_chosen_by_player=None,
                card_chosen_by_target=None,
            )

        self.end_db()


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

        assert str(nothing_effect(1)) == str(GameAction(ActionType.NOTHING))


# ============================ FLAMETHROWER EFFECT ============================


class TestFlamethrowerEffectFIRSTPLAY:
    """Tests for flamethrower effect (defense GameAction)."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def init_db(self):
        """Init DB."""
        with db_session:
            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            Player(
                id=1,
                game=Game[1],
                alive=True,
                round_position=1,
                name="Player 1",
            )
            Player(
                id=2,
                game=Game[1],
                alive=True,
                round_position=2,
                name="Player 2",
            )
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Game[1].delete()
            Deck[1].delete()
            Player[1].delete()
            Player[2].delete()
            commit()

    def test_flamethrower_effect(self):
        """Test flamethrower effect."""
        self.init_db()

        assert str(
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=3,
                target=2,
                first_play=True,
            )
        ) == str(GameAction(ActionType.ASK_DEFENSE, 2, [17]))

        self.end_db()

    def test_flamethrower_effect_without_target(self):
        """Test flamethrower effect without target."""
        self.init_db()

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=3, first_play=True)

        self.end_db()


class TestFlamethrowerEffectREAL:
    """Tests for flamethrower effect."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def init_db(self):
        """Init DB."""
        with db_session:
            Deck(id=1)
            Game(id=1, deck=Deck[1], current_phase="Play")
            Player(
                id=1,
                game=Game[1],
                alive=True,
                round_position=1,
                name="Player 1",
            )
            Player(
                id=2,
                game=Game[1],
                alive=True,
                round_position=2,
                name="Player 2",
            )
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Game[1].delete()
            Deck[1].delete()
            Player[1].delete()
            Player[2].delete()
            commit()

    @db_session
    def test_flamethrower_effect(self):
        """Test flamethrower effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        do_effect(id_game=1, id_player=1, id_card_type=3, target=2)

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=3,
                target=1,
            )
        ) == str(GameAction(ActionType.KILL, 2))

        self.end_db()

    @db_session
    def test_flamethrower_effect_without_target(self):
        """Test flamethrower effect without target."""
        self.init_db()

        Game[1].current_phase = "Play"
        do_effect(id_game=1, id_player=1, id_card_type=3, target=2)

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1, id_player=2, id_card_type=0, id_card_type_before=3
            )

        self.end_db()

    @db_session
    def test_flamethrower_effect_with_target_dead(self):
        """Test flamethrower effect with target dead."""
        self.init_db()

        Player[2].alive = False

        Game[1].current_phase = "Play"
        do_effect(id_game=1, id_player=1, id_card_type=3, target=2)

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=3,
                target=1,
            )

        self.end_db()
