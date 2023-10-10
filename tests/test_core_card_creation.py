"""Test card creation module."""
import pytest

from . import AvailableDeck
from . import Card
from . import card_names
from . import create_all_cards
from . import db_session
from . import init_available_deck
from . import quantity_cards

# ===================== INITIAL CARD FUNCTIONS =====================


class TestCardCreation:
    """Test card creation"""

    # Create cards
    @db_session
    def test_create_all_cards(self):
        """Test create all cards in the database."""
        create_all_cards()

        cnt_total_cards = 109
        cnt_total_card_for_type = [
            0,
            1,
            20,
            5,
            4,
            2,
            8,
            5,
            3,
            5,
            2,
            7,
            5,
            3,
            4,
            4,
            3,
            3,
            2,
            3,
            1,
            2,
            1,
            1,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            1,
        ]

        assert len(Card.select()) == cnt_total_cards
        for i in range(len(cnt_total_card_for_type)):
            assert (
                len(list(Card.select(idtype=i))) == cnt_total_card_for_type[i]
            )
            for x in list(Card.select(idtype=i)):
                assert x.name == card_names[i][0]
                assert x.type == card_names[i][1]

        for x in list(Card.select()):
            x.delete()

    @db_session
    def test_create_all_cards_already_created(self):
        """Test create all cards in the database."""
        create_all_cards()
        with pytest.raises(ValueError):
            create_all_cards()

        for x in list(Card.select()):
            x.delete()

    # Initialize available deck creating relationship with cards

    @db_session
    def aux_function_to_test_init_available_deck_for_cnt_players(
        self, cnt_players: int
    ):
        """Test initialize an available deck creating relationship with cards."""
        AvailableDeck(id=1)

        init_available_deck(1, cnt_players)

        cnt_total_cards = 0
        cnt_total_cards_for_type = []

        for x in quantity_cards:
            sum = 0
            for i in range(cnt_players + 1):
                sum += x[i]
            cnt_total_cards += sum
            cnt_total_cards_for_type.append(sum)

        available_cards = AvailableDeck[1].cards
        assert len(list(available_cards)) == cnt_total_cards
        for i in range(len(cnt_total_cards_for_type)):
            assert (
                len(list(available_cards.select(idtype=i)))
                == cnt_total_cards_for_type[i]  # noqa : W503
            )
            for x in list(available_cards.select(idtype=i)):
                assert x.name == card_names[i][0]
                assert x.type == card_names[i][1]

        for x in list(Card.select()):
            x.delete()
        AvailableDeck[1].delete()

    def test_init_available_deck_for_cnt_players(self):
        """
        Test initialize an available deck creating relationship with cards.
        This check the correct creation of the cards for each number of players.
        Checking the 13 possible cases.
        """
        for i in range(13):
            self.aux_function_to_test_init_available_deck_for_cnt_players(i)

    @db_session
    def aux_function_to_test_init_available_deck_for_cnt_players_with_cards_already_created(
        self, cnt_players: int
    ):
        """Test initialize an available deck creating relationship with cards."""
        AvailableDeck(id=1)
        create_all_cards()

        init_available_deck(1, cnt_players)

        cnt_total_cards = 0
        cnt_total_cards_for_type = []

        for x in quantity_cards:
            sum = 0
            for i in range(cnt_players + 1):
                sum += x[i]
            cnt_total_cards += sum
            cnt_total_cards_for_type.append(sum)

        available_cards = AvailableDeck[1].cards
        assert len(list(available_cards)) == cnt_total_cards
        for i in range(len(cnt_total_cards_for_type)):
            assert (
                len(list(available_cards.select(idtype=i)))
                == cnt_total_cards_for_type[i]  # noqa : W503
            )
            for x in list(available_cards.select(idtype=i)):
                assert x.name == card_names[i][0]
                assert x.type == card_names[i][1]

        for x in list(Card.select()):
            x.delete()
        AvailableDeck[1].delete()

    def test_init_available_deck_for_cnt_players_with_cards_already_created(
        self,
    ):
        """
        Test initialize an available deck creating relationship with cards.
        This check the correct creation of the cards for each number of players.
        Checking the 13 possible cases.
        """
        for i in range(13):
            self.aux_function_to_test_init_available_deck_for_cnt_players_with_cards_already_created(
                i
            )

    @db_session
    def test_init_available_deck_already_initialized(self):
        """Test initialize an available deck creating relationship with cards."""
        AvailableDeck(id=1)
        init_available_deck(1, 5)
        with pytest.raises(ValueError):
            init_available_deck(1, 5)

        for x in list(Card.select()):
            x.delete()
        AvailableDeck[1].delete()
