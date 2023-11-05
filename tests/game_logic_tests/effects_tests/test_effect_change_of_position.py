"""Test change of position effect."""
import pytest

from . import ActionType
from . import Card
from . import clean_db
from . import commit
from . import create_all_cards
from . import db_session
from . import Deck
from . import do_effect
from . import Game
from . import GameAction
from . import Player

# ================================== CHANGE OF POSITION ==================================


class TestChangeOfPositionFIRSTPLAY:
    """Test Change Of Position - ASK DEFENSE."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()
        create_all_cards()

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
    def test_change_of_position_effect_ask_defense(self):
        """Test Change Of Position effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=9).first())

        assert str(
            do_effect(id_game=1, id_player=1, id_card_type=9, target=2)
        ) == str(
            GameAction(
                action=ActionType.ASK_DEFENSE, target=[2], defense_cards=[13]
            )
        )

        self.end_db()

    @db_session
    def test_change_of_position_effect_without_target(self):
        """Test Change Of Position effect without target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=9).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=9)

        self.end_db()


class TestChangeOfPositionREALEFFECT:
    """Test Change Of Position - REAL EFFECT."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()
        create_all_cards()

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
    def test_change_of_position_effect(self):
        """Test Change Of Position effect."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=9).first())

        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                target=1,
                id_card_type_before=9,
            )
        ) == str(GameAction(action=ActionType.CHANGE_POSITION, target=[2, 1]))

        self.end_db()

    @db_session
    def test_change_of_position_effect_in_invalid_phase(self):
        """Test Change Of Position effect in invalid phase."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=9).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                target=1,
                id_card_type_before=9,
            )

        self.end_db()

    @db_session
    def test_change_of_position_effect_without_target(self):
        """Test Change Of Position effect without target."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=9).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1, id_player=2, id_card_type=0, id_card_type_before=9
            )

        self.end_db()

    @db_session
    def test_change_of_position_effect_with_invalid_target(self):
        """Test Change Of Position effect with invalid target."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=9).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                target=31,
                id_card_type_before=9,
            )

        self.end_db()

    @db_session
    def test_change_of_position_effect_with_dead_target(self):
        """Test Change Of Position effect with dead target."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=9).first())

        Player[1].alive = False

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                target=1,
                id_card_type_before=9,
            )

        self.end_db()

    @db_session
    def test_change_of_position_effect_with_invalid_player(self):
        """Test Change Of Position effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=9).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=31,
                id_card_type=0,
                target=1,
                id_card_type_before=9,
            )

        self.end_db()

    @db_session
    def test_change_of_position_effect_with_player_as_target(self):
        """Test Change Of Position effect with player as target."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=9).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                target=2,
                id_card_type_before=9,
            )

        self.end_db()


# ================================== CHANGE OF POSITION / YOU BETTER RUN (DEFENSE) ==================================


class TestImFineHereEffect:
    """Test I'm Fine Here effect."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()
        create_all_cards()

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
    def test_im_fine_here_effect(self):
        """Test I'm Fine Here effect."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=9).first())
        Player[2].hand.add(Card.select(idtype=13).first())

        assert str(
            do_effect(id_game=1, id_player=2, id_card_type=13, target=1)
        ) == str(GameAction(action=ActionType.NOTHING))

        self.end_db()

    @db_session
    def test_im_fine_here_effect_with_invalid_phase(self):
        """Test I'm Fine Here effect with invalid phase."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=9).first())
        Player[2].hand.add(Card.select(idtype=13).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=2, id_card_type=13, target=1)

        self.end_db()
