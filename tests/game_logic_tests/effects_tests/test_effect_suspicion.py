"""Test suspicion effect."""
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

# ================================= SUSPICION =================================


class TestSuspicionEffect:
    """Test Suspicion effect."""

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
    def test_suspicion_effect(self):
        """Test Suspicion effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=6).first())

        Player[2].hand.add(Card.select(idtype=3).first())

        assert str(
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=6,
                target=2,
                card_chosen_by_player=3,
            )
        ) == str(
            GameAction(action=ActionType.SHOW, target=[2, 1], card_target=[3])
        )

        self.end_db()

    @db_session
    def test_suspicion_effect_with_invalid_phase(self):
        """Test Suspicion effect with invalid phase."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=6).first())

        Player[2].hand.add(Card.select(idtype=3).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=6,
                target=2,
                card_chosen_by_player=3,
            )

        self.end_db()

    @db_session
    def test_suspicion_effect_without_target(self):
        """Test Suspicion effect without target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=6).first())

        Player[2].hand.add(Card.select(idtype=3).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1, id_player=1, id_card_type=6, card_chosen_by_player=3
            )

        self.end_db()

    @db_session
    def test_suspicion_effect_with_invalid_target(self):
        """Test Suspicion effect with invalid target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=6).first())

        Player[2].hand.add(Card.select(idtype=3).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=6,
                target=31,
                card_chosen_by_player=3,
            )

        self.end_db()

    @db_session
    def test_suspicion_effect_with_dead_target(self):
        """Test Suspicion effect with dead target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=6).first())

        Player[2].hand.add(Card.select(idtype=3).first())

        Player[2].alive = False

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=6,
                target=2,
                card_chosen_by_player=3,
            )

        self.end_db()

    @db_session
    def test_suspicion_effect_with_invalid_player(self):
        """Test Suspicion effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=6).first())

        Player[2].hand.add(Card.select(idtype=3).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=31,
                id_card_type=6,
                target=2,
                card_chosen_by_player=3,
            )

        self.end_db()

    @db_session
    def test_suspicion_effect_with_player_as_target(self):
        """Test Suspicion effect with player as target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=6).first())

        Player[1].hand.add(Card.select(idtype=3).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=6,
                target=1,
                card_chosen_by_player=3,
            )

        self.end_db()

    @db_session
    def test_suspicion_effect_without_target_card(self):
        """Test Suspicion effect without target card."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=6).first())

        Player[2].hand.add(Card.select(idtype=3).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=6, target=2)

        self.end_db()

    @db_session
    def test_suspicion_effect_with_target_card_that_target_doesnt_have(self):
        """Test Suspicion effect with target card that target doesn't have."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=6).first())

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=6,
                target=2,
                card_chosen_by_player=3,
            )

        self.end_db()
