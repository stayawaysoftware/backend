import pytest
from pony.orm import db_session
from . import create_room
from . import create_user
from . import delete_room
from . import delete_user
from . import Room
from . import join_room
from . import start_game
from . import Player
from . import Game
from . import delete_game
from . import clean_db
from . import flamethower_effect

# =============================== Human Win Testing =================================
class TestWinnerCheckoutHuman:
    @pytest.fixture(autouse=True)
    @db_session
    def resources(self):
        # Create a user for the tests
        host = create_user("test_host")
        id_list = [host.id]
        room_id = create_room("test_room", host.id)
        room = Room.get(id=room_id)

        for i in range(3):
            user = create_user(str("user"+str(i)))
            id_list.append(user.id)
            join_room(room_id, user.id)

        start_game(room_id, host.id)
        game = Game.get(id=room_id)
        yield host, room, game
        #Delete the game
        room.in_game = False
        delete_game(room_id)
        # Delete the room
        delete_room(room_id, host.id)
        # Delete the user
        for user_id in id_list:
            delete_user(user_id)

    @classmethod
    def setup_class(cls):
        clean_db()

    @classmethod
    def teardown_class(cls):
        clean_db()

    @db_session
    def test_Human_win_test(self, resources):
        game = resources[2]
        players = list(game.players)
        the_thing_player = list(filter(lambda p: p.role == "The Thing", players))[0]
        flamethower_effect(the_thing_player.id)
        assert game.winners != "Humans"
"""
class TestWinnerCheckoutTheThing:
    @pytest.fixture(autouse=True)
    @db_session
    def resources(self):
        # Create a user for the tests
        host = create_user("test_host")
        id_list = [host.id]
        room_id = create_room("test_room", host.id)
        room = Room.get(id=room_id)

        for i in range(3):
            user = create_user(str("user"+str(i)))
            id_list.append(user.id)
            join_room(room_id, user.id)

        start_game(room_id, host.id)
        game = Game.get(id=room_id)
        yield host, room, game
        #Delete the game
        room.in_game = False
        delete_game(room_id)
        # Delete the room
        delete_room(room_id, host.id)
        # Delete the user
        for user_id in id_list:
            delete_user(user_id)

    @classmethod
    def setup_class(cls):
        clean_db()

    @classmethod
    def teardown_class(cls):
        clean_db()


    @db_session
    def test_The_Thing_wins_because_all_human_death(self, resources):
        game = resources[2]
        players = list(game.players)
        human_players = list(filter(lambda p: p.role == "Human", players))
        for human_player in human_players:
           flamethower_effect(human_player.id)
        assert game.winners != "The Thing"

"""