"""Test functions used to all the game operation (internal logic)."""
import pytest

from . import AvailableDeck
from . import Card
from . import clean_db
from . import commit
from . import db_session
from . import Deck
from . import delete_decks
from . import discard
from . import DisposableDeck
from . import draw
from . import draw_no_panic
from . import draw_specific
from . import Game
from . import initialize_decks
from . import Player

# ===================== BASIC GAME FUNCTIONS =====================


class TestGameUtilityBasic:
    """Test basic game functions."""

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
        Game(id=1)
        for i in range(1, 13):
            Player(id=i, name=f"Player{i}", round_position=i, game=Game[1])
        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()

    @db_session
    def test_initialize_decks(self):
        """Test initialize_decks function."""
        deck = initialize_decks(1, 12)

        assert Deck.exists(id=1)
        assert AvailableDeck.exists(id=1)
        assert DisposableDeck.exists(id=1)

        assert deck == Deck[1]

        assert deck.available_deck.id == 1
        assert deck.disposable_deck.id == 1
        assert AvailableDeck[1].deck.id == 1
        assert DisposableDeck[1].deck.id == 1

        assert len(AvailableDeck[1].cards) == 109
        assert len(DisposableDeck[1].cards) == 0
        for i in range(1, 13):
            assert len(Player[i].hand) == 0

        AvailableDeck[1].delete()
        DisposableDeck[1].delete()
        Deck[1].delete()
        for i in range(0, 109):
            Card[i].delete()

    @db_session
    def test_delete_decks(self):
        """Test delete_decks function."""
        Deck(id=1)
        AvailableDeck(id=1, deck=Deck[1])
        DisposableDeck(id=1, deck=Deck[1])

        for i in range(109):
            Card(id=i, name="test", idtype=i, available_deck=AvailableDeck[1])

        commit()

        assert Deck.exists(id=1)
        assert AvailableDeck.exists(id=1)
        assert DisposableDeck.exists(id=1)

        delete_decks(1)

        assert not Deck.exists(id=1)
        assert not AvailableDeck.exists(id=1)
        assert not DisposableDeck.exists(id=1)

        for i in range(109):
            assert Card.exists(id=i)
            assert len(Card[i].available_deck) == 0

        # Erase if the test fails
        if Deck.exists(id=1):
            Deck[1].delete()
        if AvailableDeck.exists(id=1):
            AvailableDeck[1].delete()
        if DisposableDeck.exists(id=1):
            DisposableDeck[1].delete()
        for i in range(109):
            if Card.exists(id=i):
                Card[i].delete()


# ===================== GAME PHASES FUNCTIONS =====================


class TestGameUtilityPhases:
    """Test draw function."""

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
    def test_draw(self):
        """Test draw function."""
        id_player = 1
        for _ in range(2 * 109 + 1):
            Game[1].current_phase = "Draw"
            card = draw(1, id_player)

            assert Card.exists(id=card)
            assert (
                len(Card[card].players) == 1
                and Player[id_player] in Card[card].players  # noqa : W503
            )
            assert (
                len(Player[id_player].hand) == 1
                and Card[card] in Player[id_player].hand  # noqa : W503
            )
            assert len(Card[card].available_deck) == 0
            assert len(Card[card].disposable_deck) == 0
            for i in range(1, 13):
                if i != id_player:
                    assert len(Player[i].hand) == 0

            Game[1].current_phase = "Discard"
            Player[id_player].hand.remove(Card[card])
            DisposableDeck[1].cards.add(Card[card])

            id_player += 1
            if id_player > 12:
                id_player = 1

    @db_session
    def test_draw_with_invalid_player(self):
        """Test draw function with invalid player."""
        with pytest.raises(ValueError):
            draw(1, 0)

        with pytest.raises(ValueError):
            draw(1, 13)

    @db_session
    def test_draw_with_invalid_game(self):
        """Test draw function with invalid game."""
        with pytest.raises(ValueError):
            draw(2, 1)

    @db_session
    def test_draw_with_invalid_phase(self):
        """Test draw function with invalid phase."""
        Game[1].current_phase = "Play"
        with pytest.raises(ValueError):
            draw(1, 1)

        Game[1].current_phase = "Discard"
        with pytest.raises(ValueError):
            draw(1, 1)

    @db_session
    def test_draw_specific(self):
        """Test draw_specific function."""
        id_player = 1
        for idtype_required in range(1, 32):
            for _ in range(2 * 109 + 1):
                # I do this for to test several possibilities and that everything works correctly

                card = draw_specific(1, id_player, idtype_required)

                assert Card.exists(id=card)
                assert (
                    len(Card[card].players) == 1
                    and Player[id_player] in Card[card].players  # noqa : W503
                )
                assert (
                    len(Player[id_player].hand) == 1
                    and Card[card] in Player[id_player].hand  # noqa : W503
                )
                assert len(Card[card].available_deck) == 0
                assert len(Card[card].disposable_deck) == 0
                for i in range(1, 13):
                    if i != id_player:
                        assert len(Player[i].hand) == 0

                assert Card[card].idtype == idtype_required

                Player[id_player].hand.remove(Card[card])
                DisposableDeck[1].cards.add(Card[card])

    @db_session
    def test_draw_specific_with_invalid_player(self):
        """Test draw_specific function with invalid player."""
        with pytest.raises(ValueError):
            draw_specific(1, 0, 1)

        with pytest.raises(ValueError):
            draw_specific(1, 13, 1)

    @db_session
    def test_draw_specific_with_invalid_game(self):
        """Test draw_specific function with invalid game."""
        with pytest.raises(ValueError):
            draw_specific(2, 1, 1)

    @db_session
    def test_draw_specific_with_idtype_that_decks_doesnt_have(self):
        """Test draw_specific function with idtype that decks doesn't have."""
        with pytest.raises(ValueError):
            draw_specific(1, 1, 100)

        draw_specific(1, 1, 1)
        with pytest.raises(ValueError):
            draw_specific(1, 1, 1)

    @db_session
    def test_draw_no_panic(self):
        """Test draw_no_panic function."""
        id_player = 1
        for _ in range(2 * 109 + 1):
            # Draw the no panic card
            card = draw_no_panic(1, id_player)

            assert Card.exists(id=card)
            assert (
                len(Card[card].players) == 1
                and Player[id_player] in Card[card].players  # noqa : W503
            )
            assert (
                len(Player[id_player].hand) == 1
                and Card[card] in Player[id_player].hand  # noqa : W503
            )
            assert len(Card[card].available_deck) == 0
            assert len(Card[card].disposable_deck) == 0
            for i in range(1, 13):
                if i != id_player:
                    assert len(Player[i].hand) == 0
            assert Card[card].type != "PANIC"

            # Discard the card to check others
            Player[id_player].hand.remove(Card[card])
            DisposableDeck[1].cards.add(Card[card])

            id_player += 1
            if id_player > 12:
                id_player = 1

    @db_session
    def test_draw_no_panic_with_invalid_player(self):
        """Test draw_no_panic function with invalid player."""
        with pytest.raises(ValueError):
            draw_no_panic(1, 0)

        with pytest.raises(ValueError):
            draw_no_panic(1, 13)

    def test_draw_no_panic_with_invalid_game(self):
        """Test draw_no_panic function with invalid game."""
        with pytest.raises(ValueError):
            draw_no_panic(2, 1)

    @db_session
    def test_discard(self):
        """Test discard function."""
        id_player = 1
        for _ in range(2 * 109 + 1):
            if len(AvailableDeck[1].cards) == 0:
                for x in DisposableDeck[1].cards:
                    DisposableDeck[1].cards.remove(x)
                    AvailableDeck[1].cards.add(x)

            Game[1].current_phase = "Draw"
            card = AvailableDeck[1].cards.select().first().id
            AvailableDeck[1].cards.remove(Card[card])
            Player[id_player].hand.add(Card[card])

            Game[1].current_phase = "Discard"
            card_removed = discard(1, Card[card].idtype, id_player)

            assert (
                card == card_removed
            )  # Because it's random only with one card
            assert len(Card[card].players) == 0
            assert len(Player[id_player].hand) == 0
            assert len(Card[card].available_deck) == 0
            assert (
                len(Card[card].disposable_deck) == 1
                and Card[card] in DisposableDeck[1].cards  # noqa : W503
            )
            for i in range(1, 13):
                if i != id_player:
                    assert len(Player[i].hand) == 0

            id_player += 1
            if id_player > 12:
                id_player = 1

    @db_session
    def test_discard_with_invalid_game(self):
        """Test discard function with invalid game."""
        with pytest.raises(ValueError):
            discard(2, 0, 1)

    @db_session
    def test_discard_with_invalid_phase(self):
        """Test discard function with invalid phase."""
        Game[1].current_phase = "Play"
        with pytest.raises(ValueError):
            discard(1, 0, 1)

        Game[1].current_phase = "Draw"
        with pytest.raises(ValueError):
            discard(1, 0, 1)

    @db_session
    def test_discard_with_invalid_player(self):
        """Test discard function with invalid player."""
        Game[1].current_phase = "Discard"
        with pytest.raises(ValueError):
            discard(1, 0, 0)

        with pytest.raises(ValueError):
            discard(1, 0, 13)

    @db_session
    def test_discard_with_player_without_card(self):
        """Test discard function with player without card."""
        Game[1].current_phase = "Discard"
        with pytest.raises(ValueError):
            discard(1, 0, 1)

    @db_session
    def test_discard_with_player_without_card_of_that_type(self):
        """Test discard function with player without card."""
        Game[1].current_phase = "Discard"
        Player[1].hand.add(Card.select(idtype=2).first())
        Player[1].hand.add(Card.select(idtype=3).first())
        with pytest.raises(ValueError):
            discard(1, 1, 1)

    @db_session
    def test_draw_and_discard(self):
        """Test draw and discard interactions."""
        id_player = 1
        for _ in range(2 * 109 + 1):
            Game[1].current_phase = "Draw"
            card = draw(1, id_player)

            assert Card.exists(id=card)
            assert (
                len(Card[card].players) == 1
                and Player[id_player] in Card[card].players  # noqa : W503
            )
            assert (
                len(Player[id_player].hand) == 1
                and Card[card] in Player[id_player].hand  # noqa : W503
            )
            assert len(Card[card].available_deck) == 0
            assert len(Card[card].disposable_deck) == 0
            for i in range(1, 13):
                if i != id_player:
                    assert len(Player[i].hand) == 0

            Game[1].current_phase = "Discard"
            card_removed = discard(1, Card[card].idtype, id_player)

            assert (
                card == card_removed
            )  # Because it's random only with one card
            assert len(Card[card].players) == 0
            assert len(Player[id_player].hand) == 0
            assert len(Card[card].available_deck) == 0
            assert (
                len(Card[card].disposable_deck) == 1
                and Card[card] in DisposableDeck[1].cards  # noqa : W503
            )
            for i in range(1, 13):
                if i != id_player:
                    assert len(Player[i].hand) == 0

            id_player += 1
            if id_player > 12:
                id_player = 1

    @db_session
    def test_draw_and_discard_with_hand_of_4_max(self):
        """Test draw and discard interactions with hand of 4 max."""
        id_player = 1
        for _ in range(2 * 109 + 1):
            Game[1].current_phase = "Draw"
            card = draw(1, id_player)

            assert Card.exists(id=card)
            assert (
                len(Card[card].players) == 1
                and Player[id_player] in Card[card].players  # noqa : W503
            )
            assert (
                len(Player[id_player].hand) <= 5
                and len(Player[id_player].hand) > 0  # noqa : W503
                and Card[card] in Player[id_player].hand  # noqa : W503
            )
            assert len(Card[card].available_deck) == 0
            assert len(Card[card].disposable_deck) == 0
            for i in range(1, 13):
                if i != id_player:
                    assert Card[card] not in Player[i].hand

            if len(Player[id_player].hand) > 4:
                possible_cards = []
                for x in Player[id_player].hand.select(
                    idtype=Card[card].idtype
                ):
                    possible_cards.append(x.id)

                Game[1].current_phase = "Discard"
                card_removed = discard(1, Card[card].idtype, id_player)

                assert card_removed in possible_cards
                assert len(Card[card_removed].players) == 0
                assert len(Player[id_player].hand) == 4
                assert len(Card[card_removed].available_deck) == 0
                assert (
                    len(Card[card_removed].disposable_deck) == 1
                    and Card[card_removed]  # noqa : W503
                    in DisposableDeck[1].cards  # noqa : W503
                )
                for i in range(1, 13):
                    if i != id_player:
                        assert Card[card_removed] not in Player[i].hand

            id_player += 1
            if id_player > 12:
                id_player = 1
