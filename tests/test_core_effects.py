"""Test card effects logic module."""
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

        assert str(nothing_effect(1)) == str(
            GameAction(action=ActionType.NOTHING)
        )


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


# ============================ EXCHANGE EFFECT ============================


class TestExchangeEffectFIRSTPLAY:
    """Tests for exchange effect."""

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
    def test_exchange_effect_ask_defense(self):
        """Test exchange effect ask defense."""
        self.init_db()

        Game[1].current_phase = "Play"

        assert str(
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=32,
                target=2,
                card_chosen_by_player=3,
            )
        ) == str(
            GameAction(
                action=ActionType.ASK_DEFENSE,
                target=[2],
                defense_cards=[14, 15, 16],
            )
        )

        self.end_db()


class TestExchangeREALEFFECT:
    """Tests for exchange effect."""

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
    def test_exchange_effect(self):
        """Test exchange effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE, target=[1, 2], card_target=[3, 5]
            )
        )

        self.end_db()

    @db_session
    def test_exchange_effect_in_invalid_phase(self):
        """Test exchange effect in invalid phase."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Play"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_without_target(self):
        """Test exchange effect without target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_with_invalid_target(self):
        """Test exchange effect with invalid target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=100,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_with_dead_target(self):
        """Test exchange effect with dead target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        Player[2].alive = False
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=2,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_with_invalid_player(self):
        """Test exchange effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=100,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_with_player_as_target(self):
        """Test exchange effect with player as target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=5).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=1,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_without_card_chosen_by_player(self):
        """Test exchange effect without card chosen by player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_without_card_chosen_by_target(self):
        """Test exchange effect without card chosen by target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_The_Thing_card(self):
        """Test exchange effect with The Thing card."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=1,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=1,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_both_sides(self):
        """Test exchange effect with infected card both sides."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=2).first())
        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=2).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=2,
                card_chosen_by_target=2,
            )

        self.end_db()

    # INFECT CARD FROM PLAYER SIDE

    @db_session
    def test_exchange_effect_infected_card_from_player_side_with_player_as_The_Thing_and_target_as_Infected(
        self,
    ):
        """Test exchange effect with infected card from player side with player as The Thing and target as Infected."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "The Thing"
        Player[2].role = "Infected"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_player_side_with_player_as_The_Thing_and_target_as_human(
        self,
    ):
        """Test exchange effect with infected card from player side with player as The Thing and target as human."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE,
                target=[1, 2, 2],
                card_target=[2, 5],
                action2=ActionType.INFECT,
            )
        )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_player_side_with_player_as_Infected_with_only_one(
        self,
    ):
        """Test exchange effect with infected card from player side with player as Infected with only one."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_player_side_with_player_as_Infected_and_target_as_The_Thing(
        self,
    ):
        """Test exchange effect with infected card from player side with player as Infected and target as The Thing."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(Card.select(idtype=1).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE, target=[1, 2], card_target=[2, 5]
            )
        )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_player_side_with_player_as_Infected_and_target_as_Infected(
        self,
    ):
        """Test exchange effect with infected card from player side with player as Infected and target as Infected."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "Infected"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_player_side_with_player_as_Infected_and_target_as_Human(
        self,
    ):
        """Test exchange effect with infected card from player side with player as Infected and target as Human."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "Human"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_player_side_with_player_as_Human(
        self,
    ):
        """Test exchange effect with infected card from player side with player as Human."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Human"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=32,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=32,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    # INFECT CARD FROM TARGET SIDE

    @db_session
    def test_exchange_effect_infected_card_from_target_side_with_player_as_Infected_and_target_as_The_Thing(
        self,
    ):
        """Test exchange effect with infected card from target side with player as Infected and target as The Thing."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "The Thing"
        Player[2].role = "Infected"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=32,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=32,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_target_side_with_player_as_Human_and_target_as_The_Thing(
        self,
    ):
        """Test exchange effect with infected card from target side with player as Human and target as The Thing."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=32,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=32,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE,
                target=[2, 1, 2],
                card_target=[5, 2],
                action2=ActionType.INFECT,
            )
        )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_target_side_with_target_as_Infected_with_only_one(
        self,
    ):
        """Test exchange effect with infected card from target side with target as Infected with only one."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=32,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=32,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_target_side_with_player_as_The_Thing_and_target_as_Infected(
        self,
    ):
        """Test exchange effect with infected card from target side with target as Infected and player as The Thing."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(Card.select(idtype=1).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=32,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=32,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE, target=[2, 1], card_target=[5, 2]
            )
        )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_target_side_with_player_as_Infected_and_target_as_Infected(
        self,
    ):
        """Test exchange effect with infected card from target side with player as Infected and target as Infected."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "Infected"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=32,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=32,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_target_side_with_player_as_Human_and_target_as_Infected(
        self,
    ):
        """Test exchange effect with infected card from target side with target as Infected and player as Human."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "Human"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=32,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=32,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()

    @db_session
    def test_exchange_effect_infected_card_from_target_side_with_target_as_Human(
        self,
    ):
        """Test exchange effect with infected card from target side with target as Human."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Human"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=32,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=32,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()


# ================================== SEDUCTION EFFECT ==================================


class TestSeductionEffectFIRSTPLAY:
    """Tests for seduction effect."""

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
    def test_seduction_effect_ask_defense(self):
        """Test seduction effect ask defense."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=11).first())

        assert str(
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=11,
                target=2,
                card_chosen_by_player=3,
            )
        ) == str(
            GameAction(
                action=ActionType.ASK_DEFENSE,
                target=[2],
                defense_cards=[14, 15, 16],
            )
        )

        self.end_db()


class TestSeductionEffectREALEFFECT:
    """Tests for seduction effect."""

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
    def test_seduction_effect(self):
        """Test seduction effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE, target=[1, 2], card_target=[3, 5]
            )
        )

        self.end_db()

    @db_session
    def test_seduction_effect_in_invalid_phase(self):
        """Test seduction effect in invalid phase."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Play"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_without_target(self):
        """Test seduction effect without target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_with_invalid_target(self):
        """Test seduction effect with invalid target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=100,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_with_dead_target(self):
        """Test seduction effect with dead target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        Player[2].alive = False
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=2,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_with_invalid_player(self):
        """Test seduction effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=100,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_with_player_as_target(self):
        """Test seduction effect with player as target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=5).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=1,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_without_card_chosen_by_player(self):
        """Test seduction effect without card chosen by player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_without_card_chosen_by_target(self):
        """Test seduction effect without card chosen by target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_The_Thing_card(self):
        """Test seduction effect with The Thing card."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=1,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=1,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_both_sides(self):
        """Test seduction effect with infected card both sides."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=2).first())
        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=2).first())
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=2,
                card_chosen_by_target=2,
            )

        self.end_db()

    # INFECT CARD FROM PLAYER SIDE

    @db_session
    def test_seduction_effect_infected_card_from_player_side_with_player_as_The_Thing_and_target_as_Infected(
        self,
    ):
        """Test seduction effect with infected card from player side with player as The Thing and target as Infected."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "The Thing"
        Player[2].role = "Infected"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_player_side_with_player_as_The_Thing_and_target_as_human(
        self,
    ):
        """Test seduction effect with infected card from player side with player as The Thing and target as human."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE,
                target=[1, 2, 2],
                card_target=[2, 5],
                action2=ActionType.INFECT,
            )
        )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_player_side_with_player_as_Infected_with_only_one(
        self,
    ):
        """Test seduction effect with infected card from player side with player as Infected with only one."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_player_side_with_player_as_Infected_and_target_as_The_Thing(
        self,
    ):
        """Test seduction effect with infected card from player side with player as Infected and target as The Thing."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(Card.select(idtype=1).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE, target=[1, 2], card_target=[2, 5]
            )
        )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_player_side_with_player_as_Infected_and_target_as_Infected(
        self,
    ):
        """Test seduction effect with infected card from player side with player as Infected and target as Infected."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "Infected"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_player_side_with_player_as_Infected_and_target_as_Human(
        self,
    ):
        """Test seduction effect with infected card from player side with player as Infected and target as Human."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "Human"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_player_side_with_player_as_Human(
        self,
    ):
        """Test seduction effect with infected card from player side with player as Human."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Human"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=2,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=0,
                id_card_type_before=11,
                target=1,
                card_chosen_by_player=5,
                card_chosen_by_target=2,
            )

        self.end_db()

    # INFECT CARD FROM TARGET SIDE

    @db_session
    def test_seduction_effect_infected_card_from_target_side_with_player_as_Infected_and_target_as_The_Thing(
        self,
    ):
        """Test seduction effect with infected card from target side with player as Infected and target as The Thing."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "The Thing"
        Player[2].role = "Infected"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=11,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=11,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_target_side_with_player_as_Human_and_target_as_The_Thing(
        self,
    ):
        """Test seduction effect with infected card from target side with player as Human and target as The Thing."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=1).first())
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=11,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=11,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE,
                target=[2, 1, 2],
                card_target=[5, 2],
                action2=ActionType.INFECT,
            )
        )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_target_side_with_target_as_Infected_with_only_one(
        self,
    ):
        """Test seduction effect with infected card from target side with target as Infected with only one."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=11,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=11,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_target_side_with_player_as_The_Thing_and_target_as_Infected(
        self,
    ):
        """Test seduction effect with infected card from target side with target as Infected and player as The Thing."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(Card.select(idtype=1).first())
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=11,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=11,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )
        ) == str(
            GameAction(
                action=ActionType.EXCHANGE, target=[2, 1], card_target=[5, 2]
            )
        )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_target_side_with_player_as_Infected_and_target_as_Infected(
        self,
    ):
        """Test seduction effect with infected card from target side with player as Infected and target as Infected."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "Infected"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=11,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=11,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_target_side_with_player_as_Human_and_target_as_Infected(
        self,
    ):
        """Test seduction effect with infected card from target side with target as Infected and player as Human."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])
        Player[1].hand.add(infect_cards[1])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Infected"
        Player[2].role = "Human"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=11,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=11,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()

    @db_session
    def test_seduction_effect_infected_card_from_target_side_with_target_as_Human(
        self,
    ):
        """Test seduction effect with infected card from target side with target as Human."""
        self.init_db()

        Game[1].current_phase = "Play"
        infect_cards = list(Card.select(idtype=2))
        Player[1].hand.add(infect_cards[0])

        Player[2].hand.add(infect_cards[2])
        Player[2].hand.add(Card.select(idtype=5).first())

        Player[1].role = "Human"
        Player[2].role = "The Thing"

        do_effect(
            id_game=1,
            id_player=2,
            id_card_type=11,
            target=1,
            card_chosen_by_player=5,
        )

        Game[1].current_phase = "Defense"
        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=0,
                id_card_type_before=11,
                target=2,
                card_chosen_by_player=2,
                card_chosen_by_target=5,
            )

        self.end_db()


# ================================= EXCHANGE / SEDUCTION (WITH DEFENSE) =================================

# TERRIFYING


class TestTerrifyingEffect:
    """Test Terrifying effect."""

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
    def test_terrifying_effect(self):
        """Test Terrifying effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        Player[2].hand.add(Card.select(idtype=14).first())
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=14,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )
        ) == str(
            GameAction(action=ActionType.SHOW, target=[1, 2], card_target=[3])
        )

        self.end_db()

    @db_session
    def test_terrifying_effect_with_invalid_phase(self):
        """Test Terrifying effect with invalid phase."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=14,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_terrifying_effect_without_target(self):
        """Test Terrifying effect without target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=14,
                id_card_type_before=11,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_terrifying_effect_with_invalid_target(self):
        """Test Terrifying effect with invalid target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=14,
                id_card_type_before=11,
                target=31,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_terrifying_effect_with_dead_target(self):
        """Test Terrifying effect with dead target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[1].alive = False

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=14,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_terrifying_effect_with_invalid_player(self):
        """Test Terrifying effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=31,
                id_card_type=14,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_terrifying_effect_with_player_as_target(self):
        """Test Terrifying effect with player as target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=14,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_terrifying_effect_without_target_card(self):
        """Test Terrifying effect without target card."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=11).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=14,
                id_card_type_before=11,
                target=1,
            )

        self.end_db()


# NO, THANKS


class TestNoThanksEffect:
    """Test No Thanks effect."""

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
    def test_no_thanks_effect(self):
        """Test No, Thanks effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[2].hand.add(Card.select(idtype=5).first())
        Player[2].hand.add(Card.select(idtype=15).first())
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=15,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )
        ) == str(GameAction(action=ActionType.NOTHING))

        self.end_db()


# YOU FAILED


class TestYouFailedEffect:
    """Test You Failed effect."""

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
    def test_you_failed_effect(self):
        """Test You Failed effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        Player[2].hand.add(Card.select(idtype=16).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        assert str(
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=16,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )
        ) == str(
            GameAction(
                action=ActionType.ASK_EXCHANGE, target=[1, 2], card_target=[3]
            )
        )

        self.end_db()

    @db_session
    def test_you_failed_effect_with_invalid_phase(self):
        """Test You Failed effect with invalid phase."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=3).first())
        Player[1].hand.add(Card.select(idtype=11).first())

        Player[2].hand.add(Card.select(idtype=16).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=16,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_you_failed_effect_without_target(self):
        """Test You Failed effect without target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=11).first())

        Player[2].hand.add(Card.select(idtype=16).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=16,
                id_card_type_before=11,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_you_failed_effect_with_invalid_target(self):
        """Test You Failed effect with invalid target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=11).first())

        Player[2].hand.add(Card.select(idtype=16).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )
        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=16,
                id_card_type_before=11,
                target=31,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_you_failed_effect_with_dead_target(self):
        """Test You Failed effect with dead target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=11).first())

        Player[2].hand.add(Card.select(idtype=16).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"
        Player[1].alive = False

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=16,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_you_failed_effect_with_invalid_player(self):
        """Test You Failed effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=11).first())

        Player[2].hand.add(Card.select(idtype=16).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=31,
                id_card_type=16,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_you_failed_effect_with_player_as_target(self):
        """Test You Failed effect with player as target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=11).first())

        Player[2].hand.add(Card.select(idtype=16).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=1,
                id_card_type=16,
                id_card_type_before=11,
                target=1,
                card_chosen_by_target=3,
            )

        self.end_db()

    @db_session
    def test_you_failed_effect_without_target_card(self):
        """Test You Failed effect without target card."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=11).first())

        Player[2].hand.add(Card.select(idtype=16).first())

        do_effect(
            id_game=1,
            id_player=1,
            id_card_type=11,
            target=2,
            card_chosen_by_player=3,
        )

        Game[1].current_phase = "Defense"

        with pytest.raises(ValueError):
            do_effect(
                id_game=1,
                id_player=2,
                id_card_type=16,
                id_card_type_before=11,
                target=1,
            )

        self.end_db()


# ================================= ANALYSIS =================================


class TestAnalysisEffect:
    """Test Analysis effect."""

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
    def test_analysis_effect(self):
        """Test Analysis effect."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=4).first())

        assert str(
            do_effect(id_game=1, id_player=1, id_card_type=4, target=2)
        ) == str(GameAction(action=ActionType.SHOW_ALL, target=[2, 1]))

        self.end_db()

    @db_session
    def test_analysis_effect_with_invalid_phase(self):
        """Test Analysis effect with invalid phase."""
        self.init_db()

        Game[1].current_phase = "Defense"
        Player[1].hand.add(Card.select(idtype=4).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=4, target=2)

        self.end_db()

    @db_session
    def test_analysis_effect_without_target(self):
        """Test Analysis effect without target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=4).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=4)

        self.end_db()

    @db_session
    def test_analysis_effect_with_invalid_target(self):
        """Test Analysis effect with invalid target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=4).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=4, target=31)

        self.end_db()

    @db_session
    def test_analysis_effect_with_dead_target(self):
        """Test Analysis effect with dead target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=4).first())

        Player[2].alive = False

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=4, target=2)

        self.end_db()

    @db_session
    def test_analysis_effect_with_invalid_player(self):
        """Test Analysis effect with invalid player."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=4).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=31, id_card_type=4, target=2)

        self.end_db()

    @db_session
    def test_analysis_effect_with_player_as_target(self):
        """Test Analysis effect with player as target."""
        self.init_db()

        Game[1].current_phase = "Play"
        Player[1].hand.add(Card.select(idtype=4).first())

        with pytest.raises(ValueError):
            do_effect(id_game=1, id_player=1, id_card_type=4, target=1)

        self.end_db()


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
