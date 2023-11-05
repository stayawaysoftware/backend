"""Test seduction effect."""
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
                action=ActionType.EXCHANGE,
                target=[1, 2],
                card_target=[3, 5],
                exchange_phase=False,
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
                exchange_phase=False,
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
                action=ActionType.EXCHANGE,
                target=[1, 2],
                card_target=[2, 5],
                exchange_phase=False,
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
                exchange_phase=False,
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
                action=ActionType.EXCHANGE,
                target=[2, 1],
                card_target=[5, 2],
                exchange_phase=False,
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
