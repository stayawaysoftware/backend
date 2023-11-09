"""Test watch your back effect."""
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

# ================================== WATCH YOUR BACK ==================================


class TestWatchYourBack:
    """Test Watch Your Back effect."""

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
            commit()

    def end_db(self):
        """End DB."""
        with db_session:
            Game[1].delete()
            Deck[1].delete()
            Player[1].delete()
            commit()

    @db_session
    def test_watch_your_back_effect(self):
        """Test Watch Your Back effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=10).first())

        assert str(do_effect(id_game=1, id_player=1, id_card_type=10)) == str(
            GameAction(action=ActionType.REVERSE_ORDER)
        )

        self.end_db()

    @db_session
    def test_watch_your_back_effect_with_invalid_phase(self):
        """Test Watch Your Back effect with invalid phase."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=10).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=10)

        self.end_db()

    @db_session
    def test_watch_your_back_effect_with_invalid_player(self):
        """Test Watch Your Back effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=10).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=31, id_card_type=10)

        self.end_db()
