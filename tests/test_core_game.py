import pytest
from pony.orm import db_session

from . import calculate_next_turn
from . import clean_db
from . import commit
from . import create_room
from . import create_user
from . import delete_room
from . import delete_user
from . import Game
from . import init_game
from . import init_game_status
from . import join_room
from . import play_card
from . import Player
from . import turn_game_status
from . import User


class TestGame:
    @pytest.fixture()
    @db_session
    def resources(self):
        # Create a user for the tests
        user = create_user("test_user")
        # Create a room for the tests
        room = create_room("test_room", user.id)
        # Join the room
        for i in range(4):
            user2 = create_user("test_user" + str(i))
            join_room(room.id, user2.id)
        yield user, room
        # Delete the room
        delete_room(room.id, user.id)
        for i in range(4):
            delete_user(User.get(username="test_user" + str(i)).id)
        # Delete the user
        delete_user(user.id)
        # delete deck
        commit()

    @classmethod
    def setup_class(cls):
        clean_db()

    @classmethod
    def teardown_class(cls):
        clean_db()

    # Test init_game
    @db_session
    def test_init_game(self, resources):
        room = resources[1]
        init_game(room.id)
        game = Game.get(id=room.id)
        assert game is not None
        assert game.id == room.id
        assert game.round_left_direction == 0
        assert game.status == "In progress"
        assert game.current_phase == "Draw"
        assert game.current_position == 1
        assert game.players.count() >= 4 or game.players.count() <= 12
        assert game.deck is not None
        assert game.deck.id == room.id

    # Test play_card
    @db_session
    def test_play_card(self, resources):
        user = resources[0]
        room = resources[1]
        for target in room.users:
            if target.id != user.id:
                user2 = target
        init_game(room.id)
        game = Game.get(id=room.id)
        player = Player.get(id=user.id)
        hand = player.hand
        card = list(hand)[0]
        play_card(
            game_id=game.id,
            card_idtype=card.idtype,
            current_player_id=player.id,
            target_player_id=user2.id,
        )
        assert game.deck is not None
        assert game.deck.id == room.id
        assert player is not None
        assert card is not None
        if card.idtype == 3:
            assert not Player.get(id=user2.id).alive

    # Test turn_game_status
    @db_session
    def test_turn_game_status(self, resources):
        user = resources[0]
        room = resources[1]
        for target in room.users:
            if target.id != user.id:
                user2 = target
        init_game(room.id)
        game = Game.get(id=room.id)
        player = Player.get(id=user.id)
        hand = player.hand
        card = list(hand)[0]
        game_status = turn_game_status(
            game=game,
            card_idtype=card.idtype,
            current_player_id=player.id,
            target_player_id=user2.id,
        )
        assert game_status is not None
        assert game_status.players is not None
        assert game_status.alive_players is not None
        assert game_status.the_thing_is_alive is not None
        assert game_status.turn_phase is not None
        assert game_status.current_turn is not None
        assert game_status.lastPlayedCard is not None

    # Test calculate_next_turn
    @db_session
    def test_calculate_next_turn(self, resources):
        user = resources[0]
        room = resources[1]
        for target in room.users:
            if target.id != user.id:
                pass
        init_game(room.id)
        game = Game.get(id=room.id)
        player = Player.get(id=user.id)
        hand = player.hand
        list(hand)[0]
        calculate_next_turn(game_id=game.id)
        # get player with next turn
        next_player = Player.get(id=game.current_position)
        assert next_player is not None
        assert next_player.alive

    # Test init_game_status
    @db_session
    def test_init_game_status(self, resources):
        resources[0]
        room = resources[1]
        init_game(room.id)
        game = Game.get(id=room.id)
        game_status = init_game_status(game_id=game.id)
        assert game_status is not None
        assert game_status.players is not None
        assert game_status.alive_players is not None
        assert game_status.the_thing_is_alive is not None
        assert game_status.turn_phase is not None
        assert game_status.current_turn is not None
        assert game_status.lastPlayedCard is None
