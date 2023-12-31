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
from . import draw_card
from . import draw_specific
from . import flamethower_effect
from . import Game
from . import handle_defense
from . import handle_discard
from . import handle_exchange_defense
from . import join_room
from . import Player
from . import PlayerOut
from . import position_change_effect
from . import Room
from . import seduccion_effect
from . import show_hand_effect
from . import sospecha_effect
from . import start_game
from . import vigila_tus_espaldas_effect


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

        for i in range(11):
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
    @db_session
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
            game.id, card_id2, first_human.id, card_id1, second_human.id
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

    # ================================ Exchange Testing ====================================================
    @db_session
    def exchange_defended_generalized_test(
        self, resources, defense_card_idtype
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
                if card.idtype == defense_card_idtype:
                    discard(game.id, card.idtype, p.id)
        game.current_phase = "Draw"
        commit()
        # get first_human card
        first_player_card = list(first_human.hand)[0]
        card_id1 = draw_specific(game.id, second_human.id, defense_card_idtype)
        response = handle_exchange_defense(
            game.id,
            second_human.id,
            first_human.id,
            first_player_card.id,
            card_id1,
            True,
        )
        return response, card_id1, first_player_card

    @db_session
    def test_exchange_defended_by_15(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        human_players = list(filter(lambda p: p.role == "Human", players))
        second_human = human_players[1]
        (
            response,
            card_id1,
            first_player_card,
        ) = self.exchange_defended_generalized_test(resources, 15)
        has_defense = self.has_card(card_id1, second_human)
        assert not has_defense
        has_exchange_card = self.has_card(first_player_card.id, second_human)
        assert not has_exchange_card

    @db_session
    def test_exchange_defended_by_16(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        human_players = list(filter(lambda p: p.role == "Human", players))
        second_human = human_players[1]
        (
            response,
            card_id1,
            first_player_card,
        ) = self.exchange_defended_generalized_test(resources, 16)
        has_defense = self.has_card(card_id1, second_human)
        assert not has_defense
        has_exchange_card = self.has_card(first_player_card.id, second_human)
        assert not has_exchange_card

    @db_session
    def test_exchange_not_defended(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        game.current_phase = "Exchange"
        commit()
        players = list(game.players)
        first_player = players[0]
        second_player = players[1]

        Player[first_player.id].round_position = 1
        Player[second_player.id].round_position = 2

        first_player_card_id = None
        second_player_card_id = None

        for card in list(first_player.hand):
            if (
                first_player_card_id is None or first_player_card_id > card.id
            ) and card.idtype >= 3:
                first_player_card_id = card.id

        for card in list(second_player.hand):
            if (
                second_player_card_id is None
                or second_player_card_id > card.id
                and card.idtype >= 3
            ):
                second_player_card_id = card.id

        first_player_id = first_player.id
        second_player_id = second_player.id

        effect = handle_exchange_defense(
            game.id,
            first_player_id,
            second_player_id,
            second_player_card_id,
            first_player_card_id,
            False,
        )
        exchange_success = self.has_card(second_player_card_id, first_player)
        assert exchange_success
        exchange_success = self.has_card(first_player_card_id, second_player)
        assert exchange_success

    @db_session
    def test_exchange_infected_between_Thing_and_human(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        game.current_phase = "Exchange"
        commit()
        players = list(game.players)
        human_players = list(filter(lambda p: p.role == "Human", players))

        first_human_player = human_players[0]
        first_human_player.role = "The Thing"
        commit()
        second_human_player = human_players[1]
        card_id1 = draw_specific(game.id, first_human_player.id, 2)
        card_id2 = draw_specific(game.id, second_human_player.id, 3)

        Player[first_human_player.id].round_position = 1
        Player[second_human_player.id].round_position = 2
        commit()

        effect = handle_exchange_defense(
            game.id,
            first_human_player.id,
            second_human_player.id,
            card_id2,
            card_id1,
            False,
        )
        assert first_human_player.role == "The Thing"
        assert second_human_player.role == "Infected"
        first_human_player.role = "Human"
        second_human_player.role = "Human"

    @db_session
    def test_exchange_infected_between_thing_and_infected(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        game.current_phase = "Exchange"
        commit()
        players = list(game.players)
        human_players = list(filter(lambda p: p.role == "Human", players))

        first_human_player = human_players[0]
        first_human_player.role = "The Thing"
        commit()
        second_human_player = human_players[1]
        second_human_player.role = "Infected"
        commit()
        card_id1 = draw_specific(game.id, first_human_player.id, 21)
        card_id2 = draw_specific(game.id, second_human_player.id, 2)
        card_id2 = min(
            card_id2, draw_specific(game.id, second_human_player.id, 2)
        )

        Player[first_human_player.id].round_position = 1
        Player[second_human_player.id].round_position = 2

        effect = handle_exchange_defense(
            game.id,
            first_human_player.id,
            second_human_player.id,
            card_id2,
            card_id1,
            False,
        )
        assert first_human_player.role == "The Thing"
        assert second_human_player.role == "Infected"
        first_human_player.role = "Human"
        second_human_player.role = "Human"

    # ================================ Card play and effects Testing ====================================================

    @db_session
    def return_all_players_to_alive(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        for player in players:
            player.alive = True
            commit()

    @db_session
    def return_all_infected_to_human(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        for player in players:
            if player.role == "Infected":
                player.role = "Human"
                commit()

    @db_session
    def test_sospecha_effect(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        first_human_player = players[0]
        second_human_player = players[1]
        response = sospecha_effect(
            game.id, second_human_player.id, first_human_player.id
        )
        assert response is not None
        card_id = response["cards"][0]["id"]
        has_card = self.has_card(card_id=card_id, player=second_human_player)
        assert has_card

    @db_session
    def test_show_hand_effect(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        players[0]
        second_human_player = players[1]
        response = show_hand_effect(game.id, second_human_player.id)
        assert response is not None
        cards = response["cards"]
        player_hand = PlayerOut.from_player(second_human_player).model_dump(
            by_alias=True, exclude_unset=True
        )["hand"]
        has_hand = cards == player_hand
        assert has_hand

    @db_session
    def test_vigila_tus_espaldas_effect(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        game.round_left_direction = True
        commit()
        vigila_tus_espaldas_effect(game.id)
        assert not game.round_left_direction

    @db_session
    def test_position_change_effect(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        first_human_player = players[0]
        second_human_player = players[1]
        first_human_position = first_human_player.round_position
        second_human_position = second_human_player.round_position
        position_change_effect(
            game.id, first_human_player.id, second_human_player.id
        )
        assert first_human_player.round_position == second_human_position
        assert second_human_player.round_position == first_human_position

    @db_session
    def test_seduccion_effect(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        seduccion_effect(game.id)
        assert game.current_phase == "Exchange"

    @db_session
    def test_draw_card(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        first_human_player = players[0]
        game.current_phase = "Draw"
        commit()
        response = draw_card(game.id, first_human_player.id)
        assert response is not None
        has_card = self.has_card(
            response["new_card"]["id"], first_human_player
        )
        assert has_card

    @db_session
    def test_handle_discard(self, resources):
        room = resources[1]
        game = Game.get(id=room.id)
        players = list(game.players)
        first_human_player = players[0]
        first_human_player.alive = True
        first_human_card = list(first_human_player.hand)[0].idtype
        handle_discard(game.id, first_human_card, first_human_player.id)
        has_card = self.has_card(first_human_card, first_human_player)
        assert not has_card
