"""Module to test the core.player module."""
from pony.orm import commit
from pony.orm import db_session

from . import clean_db
from . import Game
from . import get_alive_neighbors
from . import Player


class TestGetAliveNeighbors:
    """Test the get_alive_neighbors function."""

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
        Game(id=1, current_phase="Draw")
        for i in range(1, 13):
            Player(
                id=2 * i,
                name=f"Player{i}",
                round_position=i,
                game=Game[1],
                alive=True,
            )

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].delete()
        for i in range(1, 13):
            Player[2 * i].delete()
        commit()

    def test_get_alive_neighbors_all_alive(self):
        """Test get_alive_neighbors."""

        # Because the players' id's were set with a *2 to check that the position is used and not the id, then the cases will contain that 2*.
        assert get_alive_neighbors(1, 2 * 1) == [2 * 12, 2 * 2]
        assert get_alive_neighbors(1, 2 * 2) == [2 * 1, 2 * 3]
        assert get_alive_neighbors(1, 2 * 3) == [2 * 2, 2 * 4]
        assert get_alive_neighbors(1, 2 * 4) == [2 * 3, 2 * 5]
        assert get_alive_neighbors(1, 2 * 5) == [2 * 4, 2 * 6]
        assert get_alive_neighbors(1, 2 * 6) == [2 * 5, 2 * 7]
        assert get_alive_neighbors(1, 2 * 7) == [2 * 6, 2 * 8]
        assert get_alive_neighbors(1, 2 * 8) == [2 * 7, 2 * 9]
        assert get_alive_neighbors(1, 2 * 9) == [2 * 8, 2 * 10]
        assert get_alive_neighbors(1, 2 * 10) == [2 * 9, 2 * 11]
        assert get_alive_neighbors(1, 2 * 11) == [2 * 10, 2 * 12]
        assert get_alive_neighbors(1, 2 * 12) == [2 * 11, 2 * 1]

    @db_session
    def test_get_alive_neighbors_with_random_dead_players(self):
        """Test get_alive_neighbors with random dead players."""

        Player[2 * 1].alive = False
        Player[2 * 5].alive = False
        Player[2 * 11].alive = False

        assert get_alive_neighbors(1, 2 * 1) == [2 * 12, 2 * 2]
        assert get_alive_neighbors(1, 2 * 2) == [2 * 12, 2 * 3]
        assert get_alive_neighbors(1, 2 * 3) == [2 * 2, 2 * 4]
        assert get_alive_neighbors(1, 2 * 4) == [2 * 3, 2 * 6]
        assert get_alive_neighbors(1, 2 * 5) == [2 * 4, 2 * 6]
        assert get_alive_neighbors(1, 2 * 6) == [2 * 4, 2 * 7]
        assert get_alive_neighbors(1, 2 * 7) == [2 * 6, 2 * 8]
        assert get_alive_neighbors(1, 2 * 8) == [2 * 7, 2 * 9]
        assert get_alive_neighbors(1, 2 * 9) == [2 * 8, 2 * 10]
        assert get_alive_neighbors(1, 2 * 10) == [2 * 9, 2 * 12]
        assert get_alive_neighbors(1, 2 * 11) == [2 * 10, 2 * 12]
        assert get_alive_neighbors(1, 2 * 12) == [2 * 10, 2 * 2]

    @db_session
    def test_get_alive_neighbors_with_one_alive_player(self):
        """Test get_alive_neighbors with only one alive player."""

        for i in range(1, 13):
            if i != 6:
                Player[2 * i].alive = False

        assert get_alive_neighbors(1, 2 * 1) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 2) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 3) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 4) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 5) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 6) == []
        assert get_alive_neighbors(1, 2 * 7) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 8) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 9) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 10) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 11) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 12) == [2 * 6, 2 * 6]

    @db_session
    def test_get_alive_neighbors_with_two_alive_players(self):
        """Test get_alive_neighbors with two alive players."""

        for i in range(1, 13):
            if i != 6 and i != 7:
                Player[2 * i].alive = False

        assert get_alive_neighbors(1, 2 * 1) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 2) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 3) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 4) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 5) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 6) == [2 * 7, 2 * 7]
        assert get_alive_neighbors(1, 2 * 7) == [2 * 6, 2 * 6]
        assert get_alive_neighbors(1, 2 * 8) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 9) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 10) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 11) == [2 * 7, 2 * 6]
        assert get_alive_neighbors(1, 2 * 12) == [2 * 7, 2 * 6]

    @db_session
    def test_get_alive_neighbors_with_no_alive_player(self):
        """Test get_alive_neighbors with no alive player."""

        for i in range(1, 13):
            Player[2 * i].alive = False

        assert get_alive_neighbors(1, 2 * 1) == []
        assert get_alive_neighbors(1, 2 * 2) == []
        assert get_alive_neighbors(1, 2 * 3) == []
        assert get_alive_neighbors(1, 2 * 4) == []
        assert get_alive_neighbors(1, 2 * 5) == []
        assert get_alive_neighbors(1, 2 * 6) == []
        assert get_alive_neighbors(1, 2 * 7) == []
        assert get_alive_neighbors(1, 2 * 8) == []
        assert get_alive_neighbors(1, 2 * 9) == []
        assert get_alive_neighbors(1, 2 * 10) == []
        assert get_alive_neighbors(1, 2 * 11) == []
        assert get_alive_neighbors(1, 2 * 12) == []
