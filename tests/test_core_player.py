import pytest
from pony.orm import db_session

from . import Card
from . import commit
from . import create_room
from . import create_user
from . import db
from . import delete_game
from . import delete_user
from . import Game
from . import init_game
from . import join_room
from . import Player
from . import User


class TestPlayer:
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
        # Create a game for the tests
        init_game(room.id)
        yield user, room
        # Delete the game
        delete_game(room.id)
        for i in range(4):
            delete_user(User.get(username="test_user" + str(i)).id)
        # Delete the user
        delete_user(user.id)
        # delete deck
        commit()

    # Test teardown
    @classmethod
    def tearDownClass(cls):
        db.drop_all_tables(with_all_data=True)

    # Test the player creation
    @db_session
    def test_create_player(self, resources):
        # Check if the player was created
        resources[0]
        room = resources[1]
        game = Game.get(id=room.id)
        for player in game.players:
            assert player is not None
        # Check if the player has been created with the correct username
        for player in game.players:
            assert player.name is not None
        # Check if the player has been saved in the database
        for player in game.players:
            assert Player.get(name=player.name) is not None
        # Check if the player has right position
        for player in game.players:
            assert player.round_position > 0 and player.round_position <= 12
        # Check if the player role is "The thing" or "Human"
        for player in game.players:
            assert player.role == "The Thing" or player.role == "Human"
        # Check if the player is alive
        for player in game.players:
            assert player.alive
        # Check if every player id is the same that the user id
        for player in game.players:
            assert player.id == User.get(username=player.name).id

    # Test card dealing
    @db_session
    def test_card_dealing(self, resources):
        # Check if the player has been dealt 5 cards
        resources[0]
        room = resources[1]
        game = Game.get(id=room.id)
        # Check if the player has been dealt the right cards
        for player in game.players:
            for card in player.hand:
                assert Card.get(id=card.id) is not None
        # Check if the player has the right number of cards
        for player in game.players:
            assert len(player.hand) == 4 or len(player.hand) == 5
