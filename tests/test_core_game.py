import pytest
from pony.orm import commit
from pony.orm import db_session

from . import check_winners
from . import clean_db
from . import create_room
from . import create_user
from . import delete_room
from . import delete_user
from . import discard
from . import draw_specific
from . import flamethower_effect
from . import Game
from . import handle_defense
from . import join_room
from . import PlayerOut
from . import Room
from . import start_game


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
            user = create_user(str("user" + str(i)))
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
        the_thing_player = list(
            filter(lambda p: p.role == "The Thing", players)
        )[0]
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
        # Set alive all the human killed for next test
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
        # Set Human roles for all the previous infected players
        infected_players = list(
            filter(lambda p: p.role == "Infected", players)
        )
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
        # Set Human roles for all the previous infected players
        infected_players = list(
            filter(lambda p: p.role == "Infected", players)
        )
        for infected_player in infected_players:
            infected_player.role = "Human"
            commit()
        assert game.winners != "None"
        assert game.winners == "The Thing"
        assert game.status == "Finished"

    # =============================== Defense testing =================================

    def generalized_test_for_defended_card(
        self, resources, idtype_attack, idtype_defense
    ):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        human_players = list(filter(lambda p: p.role == "Human", players))
        first_human = human_players[0]
        second_human = human_players[1]
        first_human.alive = True
        second_human.alive = True
        game.current_phase = "Discard"
        commit()
        for p in players:
            phand_list = list(p.hand)
            for card in phand_list:
                if card.idtype == idtype_attack:
                    discard(game.id, card.idtype, p.id)
                if card.idtype == idtype_defense:
                    discard(game.id, card.idtype, p.id)
        game.current_phase = "Draw"
        commit()
        card_id1 = draw_specific(game.id, first_human.id, idtype_attack)
        card_id2 = draw_specific(game.id, second_human.id, idtype_defense)
        response = handle_defense(
            game.id, card_id1, second_human.id, card_id2, first_human.id
        )

        return response, human_players, card_id1, card_id2

    def has_card(self, card_id, player):
        player = PlayerOut.from_player(player).model_dump(
            by_alias=True, exclude_unset=True
        )
        has_card = False
        for card in player["hand"]:
            if card["id"] == card_id:
                has_card = True
        return has_card

    @db_session
    def test_defended_card_flamethower(self, resources):
        (
            response,
            human_players,
            card_id1,
            card_id2,
        ) = self.generalized_test_for_defended_card(resources, 3, 17)
        has_card = self.has_card(card_id1, human_players[0])
        assert not has_card
        has_card = self.has_card(card_id2, human_players[1])
        assert human_players[1].alive
        assert response is not None

    @db_session
    def test_defended_card_change_position(self, resources):
        (
            response,
            human_players,
            card_id1,
            card_id2,
        ) = self.generalized_test_for_defended_card(resources, 9, 13)
        has_card = self.has_card(card_id1, human_players[0])
        assert not has_card
        has_card = self.has_card(card_id2, human_players[1])
        assert not has_card
        assert response is not None

    @db_session
    def test_defended_card_seduction_by_15(self, resources):
        (
            response,
            human_players,
            card_id1,
            card_id2,
        ) = self.generalized_test_for_defended_card(resources, 11, 15)
        has_card = self.has_card(card_id1, human_players[0])
        assert not has_card
        has_card = self.has_card(card_id2, human_players[1])
        assert not has_card
        assert response is not None

    @db_session
    def test_defended_card_seduction_by_16(self, resources):
        (
            response,
            human_players,
            card_id1,
            card_id2,
        ) = self.generalized_test_for_defended_card(resources, 11, 16)
        has_card = self.has_card(card_id1, human_players[0])
        assert not has_card
        has_card = self.has_card(card_id2, human_players[1])
        assert not has_card
        assert response is not None

    @db_session
    def test_defended_card_you_better_run(self, resources):
        (
            response,
            human_players,
            card_id1,
            card_id2,
        ) = self.generalized_test_for_defended_card(resources, 12, 13)
        has_card = self.has_card(card_id1, human_players[0])
        assert not has_card
        has_card = self.has_card(card_id2, human_players[1])
        assert not has_card
        assert response is not None
