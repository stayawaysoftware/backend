"""Test flamethrower effect."""
from . import clean_db
from . import commit
from . import db_session
from . import Deck
from . import delete_decks
from . import discard
from . import Game
from . import initialize_decks
from . import Player

# ============================ FLAMETHROWER EFFECT ============================


class TestFlamethrower:
    """Tests for flamethrower effect"""

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

        # draw_specific(id_game=1, id_player=1, idtype_card=1)

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


# ============================ FLAMETHROWER EFFECT (WITH DEFENSE) ============================


class TestNoBarbacues:
    """Tests for no barbacues effect."""

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

        # draw_specific(id_game=1, id_player=1, idtype_card=1)

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
