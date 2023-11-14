"""Test game effects."""
import pytest

from . import clean_db
from . import commit
from . import db_session
from . import Deck
from . import delete_decks
from . import discard
from . import draw_specific
from . import Game
from . import get_defense_cards
from . import initialize_decks
from . import play
from . import Player


class TestPlayInvalidOptions:
    """Test Play Function with invalid options."""

    @classmethod
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
        initialize_decks(id_game=1, quantity_players=12)
        Game(id=1, current_phase="Defense", deck=Deck[1])
        for i in range(1, 13):
            Player(
                id=i,
                name=f"Player{i}",
                round_position=i,
                game=Game[1],
                alive=True,
            )

        draw_specific(id_game=1, id_player=1, idtype_card=1)
        draw_specific(id_game=1, id_player=1, idtype_card=2)
        draw_specific(id_game=1, id_player=1, idtype_card=3)

        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].current_phase = "Discard"
        discard(id_game=1, id_player=1, idtype_card=1)
        discard(id_game=1, id_player=1, idtype_card=2)
        discard(id_game=1, id_player=1, idtype_card=3)

        delete_decks(id_game=1)
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()

    # Game doesn't exist
    def test_game_doesnt_exist(self):
        """Test game doesn't exist."""

        with pytest.raises(ValueError):
            play(
                id_game=2,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=3,
                idtype_defense_card=0,
            )

    # Player doesn't exist
    def test_player_doesnt_exist(self):
        """Test player doesn't exist."""

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=13,
                defense_player_id=2,
                idtype_attack_card=3,
                idtype_defense_card=0,
            )

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=13,
                idtype_attack_card=3,
                idtype_defense_card=0,
            )

    # Card is not in hand
    def test_card_is_not_in_hand(self):
        """Test card is not in hand."""

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=4,
                idtype_defense_card=0,
            )

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=3,
                idtype_defense_card=17,
            )

    # Cards chosen by attacker and defender are not in hand
    def test_cards_chosen_by_attacker_and_defender_are_not_in_hand(self):
        """Test cards chosen by attacker and defender are not in hand."""

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=0,
                card_chosen_by_attacker=4,
            )

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=0,
                card_chosen_by_defender=4,
            )

    # The Thing and Infected cards cannot be played
    def test_the_thing_and_infected_cards_cannot_be_played(self):
        """Test the thing and infected cards cannot be played."""

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=1,
                idtype_defense_card=0,
            )

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=2,
                idtype_defense_card=0,
            )

    # Defense card is not a defense card of the attack card
    def test_defense_card_is_not_a_defense_card(self):
        """Test defense card is not a defense card."""

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=3,
                idtype_defense_card=18,
            )

    # Attack card is not an attack card
    def test_attack_card_is_not_an_attack_card(self):
        """Test attack card is not an attack card."""

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=18,
                idtype_defense_card=0,
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
