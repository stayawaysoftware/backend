import pytest
from pony.orm import db_session
from pony.orm import commit
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
from . import check_winners


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
        yield host, room
        # Delete the room
        room.in_game = False
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
        room = resources[1]
        game = Game.get(id=room.id)
        game.winners = "None"
        game.status = "In progress"
        commit()
        players = list(game.players)
        the_thing_player = list(filter(lambda p: p.role == "The Thing", players))[0]
        flamethower_effect(the_thing_player.id)
        check_winners(game.id)
        # Return the thing to the game for next test
        the_thing_player.alive = True
        commit()
        assert game.winners == "Humans"
        assert game.status == "Finished"

    @db_session
    def test_The_Thing_wins_because_all_human_death(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        game.winners = "None"
        game.status = "In progress"
        commit()
        players = list(game.players)
        human_players = list(filter(lambda p: p.role == "Human", players))
        for human_player in human_players:
           flamethower_effect(human_player.id)
        check_winners(game.id)
        #Set alive all the human killed for next test
        for player in players:
            player.alive = True
            commit()
        assert game.winners == "The Thing"
        assert game.status == "Finished"

    @db_session
    def test_The_Thing_wins_because_infected(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        game.winners = "None"
        game.status = "In progress"
        commit()
        players = list(game.players)
        human_players = list(filter(lambda p: p.role == "Human", players))
        for human_player in human_players:
            human_player.role = "Infected"
            commit()
        check_winners(game.id)
        #Set Human roles for all the previous infected players
        infected_players = list(filter(lambda p: p.role == "Infected", players))
        for infected_player in infected_players:
            infected_player.role = "Human"
            commit()
        assert game.winners == "The Thing"
        assert game.status == "Finished"

    @db_session
    def test_The_Thing_wins_because_infected_with_a_death(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        game.winners = "None"
        game.status = "In progress"
        commit()
        human_players = list(filter(lambda p: p.role == "Human", players))
        # Kill one human
        flamethower_effect(human_players[0].id)
        for human_player in human_players:
            if human_player.alive:
                human_player.role = "Infected"
                commit()
        check_winners(game.id)
        #Set Human roles for all the previous infected players
        infected_players = list(filter(lambda p: p.role == "Infected", players))
        for infected_player in infected_players:
            infected_player.role = "Human"
            commit()
        assert game.winners == "The Thing"
        assert game.status == "Finished"

        