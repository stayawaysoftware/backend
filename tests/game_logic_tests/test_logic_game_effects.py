"""Test game effects."""
import pytest

from . import AvailableDeck
from . import Card
from . import clean_db
from . import commit
from . import db_session
from . import Deck
from . import DisposableDeck
from . import do_effect
from . import Game
from . import get_defense_cards
from . import initialize_decks
from . import play
from . import Player


class TestPlay:
    """Test Play Function."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    @db_session
    def setup_method(self):
        """Setup method."""
        Game(id=1, current_phase="Draw")
        for i in range(1, 13):
            Player(id=i, name=f"Player{i}", round_position=i, game=Game[1])
        initialize_decks(1, 12)
        Game[1].deck = Deck[1]
        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        Deck[1].delete()
        AvailableDeck[1].delete()
        DisposableDeck[1].delete()
        for i in range(0, 109):
            Card[i].delete()
        commit()

    @db_session
    def test_play(self):
        """Test play function."""
        Game[1].current_phase = "Play"
        for i in range(0, 109):
            Player[1].hand.add(Card[i])

        for i in range(0, 109):
            try:
                action = play(
                    id_game=1,
                    id_player=1,
                    idtype_card=Card[i].idtype,
                    target=2,
                )
                assert str(action) == str(
                    do_effect(
                        id_game=1,
                        id_player=1,
                        id_card_type=Card[i].idtype,
                        target=2,
                    )
                )
            except ValueError:
                with pytest.raises(ValueError):
                    do_effect(
                        id_game=1,
                        id_player=1,
                        id_card_type=Card[i].idtype,
                        target=2,
                    )

    @db_session
    def test_play_with_invalid_game(self):
        """Test play function with invalid game."""
        Game[1].current_phase = "Play"

        with pytest.raises(ValueError):
            play(id_game=2, id_player=1, idtype_card=Card[0].idtype, target=2)

    @db_session
    def test_play_with_invalid_phase(self):
        """Test play function with invalid phase."""
        Game[1].current_phase = "Draw"

        with pytest.raises(ValueError):
            play(id_game=1, id_player=1, idtype_card=Card[0].idtype, target=2)

        Game[1].current_phase = "Discard"

        with pytest.raises(ValueError):
            play(id_game=1, id_player=1, idtype_card=Card[0].idtype, target=2)

    @db_session
    def test_play_with_invalid_player(self):
        """Test play function with invalid player."""
        Game[1].current_phase = "Play"

        with pytest.raises(ValueError):
            play(id_game=1, id_player=0, idtype_card=Card[0].idtype, target=2)

        with pytest.raises(ValueError):
            play(id_game=1, id_player=13, idtype_card=Card[0].idtype, target=2)

    @db_session
    def test_play_with_invalid_card(self):
        """Test play function with invalid card."""
        Game[1].current_phase = "Play"

        with pytest.raises(ValueError):
            play(id_game=1, id_player=1, idtype_card=100, target=2)

    @db_session
    def test_play_with_invalid_target(self):
        """Test play function with invalid target."""
        Game[1].current_phase = "Play"

        with pytest.raises(ValueError):
            play(id_game=1, id_player=1, idtype_card=Card[0].idtype, target=0)

        with pytest.raises(ValueError):
            play(id_game=1, id_player=1, idtype_card=Card[0].idtype, target=13)

    @db_session
    def test_play_with_invalid_card_type_before(self):
        """Test play function with invalid card_type_before."""
        Game[1].current_phase = "Play"
        Player[1].hand.add(Card[0])

        with pytest.raises(ValueError):
            play(
                id_game=1,
                id_player=1,
                idtype_card=Card[0].idtype,
                idtype_card_before=100,
                target=2,
            )

    @db_session
    def test_play_with_invalid_card_chosen_by_player(self):
        """Test play function with invalid card_chosen_by_player."""
        Game[1].current_phase = "Play"
        Player[1].hand.add(Card[0])

        with pytest.raises(ValueError):
            play(
                id_game=1,
                id_player=1,
                idtype_card=Card[0].idtype,
                card_chosen_by_player=100,
                target=2,
            )

    @db_session
    def test_play_with_invalid_card_chosen_by_target(self):
        """Test play function with invalid card_chosen_by_target."""
        Game[1].current_phase = "Play"
        Player[1].hand.add(Card[0])

        with pytest.raises(ValueError):
            play(
                id_game=1,
                id_player=1,
                idtype_card=Card[0].idtype,
                card_chosen_by_target=100,
                target=2,
            )


class TestGetDefense:
    """Test Get Defense Function."""

    @classmethod
    @db_session
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    def test_get_defense(self):
        """Test get defense function."""

        obtained_defense_cards = []
        for i in range(0, 33):
            obtained_defense_cards.append(get_defense_cards(i))

        assert obtained_defense_cards == [
            [],  # None 0 --> Fictional card
            [],  # The Thing 1
            [],  # Infected 2
            [17],  # Flamethrower 3
            [],  # Analysis 4
            [],  # Axe 5
            [],  # Suspicion 6
            [],  # Determination 7
            [],  # Whisky 8
            [13],  # Change of position 9
            [],  # Watch your back 10
            [14, 15, 16],  # Seduction 11
            [13],  # You better run 12
            [],  # I'm fine here 13
            [],  # Terrifying 14
            [],  # No, thanks 15
            [],  # You failed 16
            [],  # No Barbecues 17
            [],  # Quarantine 18
            [],  # Locked Door 19
            [],  # Revelations 20
            [],  # Rotten ropes 21
            [],  # Get out of here 22
            [],  # Forgetful 23
            [],  # One, two... 24
            [],  # Three, four... 25
            [],  # Is the party here? 26
            [],  # Let it stay between us 27
            [],  # Turn and turn 28
            [],  # Can't we be friends? 29
            [],  # Blind date 30
            [],  # Ups! 31
            [14, 15, 16],  # Exchange 32 --> Fictional card
        ]

    def test_get_defense_with_invalid_card(self):
        """Test get defense function with invalid card."""

        with pytest.raises(ValueError):
            get_defense_cards(-1)

        with pytest.raises(ValueError):
            get_defense_cards(33)