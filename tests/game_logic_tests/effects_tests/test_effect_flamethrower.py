"""Test flamethrower effect."""
import pytest

from . import ActionType
from . import clean_db
from . import commit
from . import db_session
from . import Deck
from . import do_effect
from . import Game
from . import GameAction
from . import Player

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
        ) == str(
            GameAction(
                action=ActionType.ASK_DEFENSE, target=[2], defense_cards=[17]
            )
        )

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
        ) == str(GameAction(action=ActionType.KILL, target=[2]))

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


# ============================ FLAMETHROWER EFFECT (WITH DEFENSE) ============================


class TestNoBarbacuesEffect:
    """Tests for no barbacues effect."""

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
    def test_no_barbacues_effect(self):
        """Test no barbacues effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        do_effect(
            id_game=1, id_player=1, id_card_type=3, target=2
        )  # Play flamethrower

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=17,
                id_card_type_before=3,
                target=1,
            )
        ) == str(GameAction(action=ActionType.NOTHING))

        self.end_db()

    @db_session
    def test_no_barbacues_effect_in_invalid_phase(self):
        """Test no barbacues effect in invalid phase."""
        self.init_db()

        Game[1].current_phase = "Play"
        do_effect(
            id_game=1, id_player=1, id_card_type=3, target=2
        )  # Play flamethrower

        Game[1].current_phase = "Play"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=17,
                id_card_type_before=3,
                target=1,
            )

        self.end_db()
