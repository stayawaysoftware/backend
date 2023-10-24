from pony.orm import commit
from pony.orm import db_session

from . import AvailableDeck
from . import Card
from . import clean_db
from . import Deck
from . import DisposableDeck
from . import Game
from . import Player
from . import Room
from . import User

# Create the needed constants for the tests
ROOM_NAME = "test_room"
USER_NAME = "test_user"
NOT_EXISTS_ID = 50


class TestModels:
    @classmethod
    def setup_class(cls):
        clean_db()

    @classmethod
    def teardown_class(cls):
        clean_db()

    # Test the user model
    @db_session
    def test_user_model(self):
        # Create a user for the tests
        user = User(username=USER_NAME)
        commit()
        # Check if the user has been created
        assert user is not None
        # Check if the user has been created with the correct username
        assert user.username == USER_NAME
        # Check if the user has an id greater than 0
        assert user.id > 0
        # Check if the user has a room field set to None
        assert user.room is None
        # Check if the user has been saved in the database
        assert User.exists(username=USER_NAME)
        # Delete the user
        user.delete()
        commit()

    # Test the room model
    @db_session
    def test_room_model(self):
        # Create a user for the tests
        user = User(username=USER_NAME)
        commit()
        # Create a room for the tests
        room = Room(
            name=ROOM_NAME,
            pwd=None,
            host_id=user.id,
            in_game=False,
            min_users=4,
            max_users=12,
        )
        user.room = room
        commit()
        # Check if the room has been created
        assert room is not None
        # Check if the room has been created with the correct name
        assert room.name == ROOM_NAME
        # Check if the room has an id greater than 0

        # Check if the room has a host field set to the user created
        assert room.host_id == user.id
        # Check if the room has a in_game field set to False
        assert room.in_game is False
        # Check if the room has a min_users int field with value between 4 and 12
        assert room.min_users >= 4 and room.min_users <= 12
        # Check if the room has a max_users int field with value between 4 and 12
        assert room.max_users >= 4 and room.max_users <= 12
        # Check if the room has a pwd string field set to some value or None
        assert room.pwd is None or isinstance(room.pwd, str)
        # Check if the room has a users field with the host user
        assert len(room.users) == 1
        assert user in room.users
        # Check if the room has been saved in the database
        assert Room.exists(name=ROOM_NAME)
        # Leave user from room
        user.room = None
        commit()
        # Delete the room
        room.delete()
        # Delete the user
        user.delete()
        commit()

    # Test the game model
    @db_session
    def test_game_model(self):
        # Create a user for the tests
        user = User(username=USER_NAME)
        commit()
        # Create a room for the tests
        room = Room(
            name=ROOM_NAME,
            pwd=None,
            host_id=user.id,
            in_game=False,
            min_users=4,
            max_users=12,
        )
        user.room = room
        commit()
        # Create a game for the tests
        game = Game(
            id=room.id,
            round_left_direction=False,
            status="Waiting",
            current_phase="Draw",
            current_position=1,
        )
        commit()
        # Check if the game has been created
        assert game is not None
        # Check if the game has been created with the correct room_id
        assert game.id == room.id
        # Check if the game has been created with the correct round_left_direction
        assert game.round_left_direction is False
        # Check if the game has been created with the correct status
        assert game.status == "Waiting"
        # Check if the game has been created with the correct current_phase
        assert game.current_phase == "Draw"
        # Check if the game has been created with the correct current_position
        assert game.current_position == 1
        # Check if the game has been saved in the database
        assert Game.exists(id=room.id)
        # Delete the game
        game.delete()
        # Delete the room
        room.delete()
        # Delete the user
        user.delete()
        commit()

    # Test the player model
    @db_session
    def test_player_model(self):
        # Create a user for the tests
        user = User(username=USER_NAME)
        commit()
        # Create a room for the tests
        room = Room(
            name=ROOM_NAME,
            pwd=None,
            host_id=user.id,
            in_game=False,
            min_users=4,
            max_users=12,
        )
        user.room = room
        commit()
        # Create a game for the tests
        game = Game(
            id=room.id,
            round_left_direction=False,
            status="Waiting",
            current_phase="Draw",
            current_position=1,
        )
        commit()
        # Create a player for the tests
        player = Player(
            id=user.id,
            role="Human",
            name=user.username,
            round_position=1,
            alive=True,
            game=game,
            hand=Card(
                id=0,
                idtype=0,
                name="test_card",
                type="Action",
            ),
        )
        commit()
        # Check if the player has been created
        assert player is not None
        # Check if the player has been created with the correct id
        assert player.id == user.id
        # Check if the player has been created with the correct game
        assert list(player.game)[0] == game
        # Check if the player has been created with the correct position
        assert player.round_position == 1
        # Check if the player has been created with the correct hand
        assert player.hand is not None
        # Check if the player has been created with the correct role
        assert player.role == "Human"
        # Check if the player has been created with the correct name
        assert player.name == user.username
        # Check if the player has been created with the correct alive
        assert player.alive is True
        # Check if the player has been saved in the database
        assert Player.exists(id=user.id)
        # Delete the player
        player.delete()
        # Delete the game
        game.delete()
        # Delete the room
        room.delete()
        # Delete the user
        user.delete()
        commit()

    # Test the deck model
    @db_session
    def test_deck_model(self):
        # Create a deck for the tests
        deck = Deck(
            id=0,
            available_deck=None,
            disposable_deck=None,
            game=None,
        )
        commit()
        # Check if the deck has been created
        assert deck is not None
        # Check if the deck has been created with the correct id
        assert deck.id == 0
        # Check if the deck has been created with the correct available_deck
        assert deck.available_deck is None
        # Check if the deck has been created with the correct disposable_deck
        assert deck.disposable_deck is None
        # Check if the deck has been created with the correct game
        assert deck.game is None
        # Check if the deck has been saved in the database
        assert Deck.exists(id=0)
        # Delete the deck
        deck.delete()
        commit()

    # Test the card model
    @db_session
    def test_card_model(self):
        # Create a card for the tests
        card = Card(
            id=10,
            idtype=0,
            name="test_card",
            type="Action",
        )
        commit()
        # Check if the card has been created
        assert card is not None
        # Check if the card has been created with the correct id
        assert card.id == 10
        # Check if the card has been created with the correct idtype
        assert card.idtype == 0
        # Check if the card has been created with the correct name
        assert card.name == "test_card"
        # Check if the card has been created with the correct type
        assert card.type == "Action"
        # Check if the card has been saved in the database
        assert Card.exists(id=0)
        # Delete the card
        card.delete()
        commit()

    # Test the available_deck model
    @db_session
    def test_available_deck_model(self):
        # Create a available_deck for the tests
        available_deck = AvailableDeck(
            id=0,
            cards=Card(
                id=50,
                idtype=0,
                name="test_card",
                type="Action",
            ),
            deck=None,
        )
        commit()
        # Check if the available_deck has been created
        assert available_deck is not None
        # Check if the available_deck has been created with the correct id
        assert available_deck.id == 0
        # Check if the available_deck has been created with the correct cards
        assert available_deck.cards is not None
        # Check if the available_deck has been created with the correct deck
        assert available_deck.deck is None
        # Check if the available_deck has been saved in the database
        assert AvailableDeck.exists(id=0)
        # Delete the available_deck
        available_deck.delete()
        commit()

    # Test the disposable_deck model
    @db_session
    def test_disposable_deck_model(self):
        # Create a disposable_deck for the tests
        disposable_deck = DisposableDeck(
            id=0,
            cards=Card(
                id=100,
                idtype=0,
                name="test_card",
                type="Action",
            ),
            deck=None,
        )
        commit()
        # Check if the disposable_deck has been created
        assert disposable_deck is not None
        # Check if the disposable_deck has been created with the correct id
        assert disposable_deck.id == 0
        # Check if the disposable_deck has been created with the correct cards
        assert disposable_deck.cards is not None
        # Check if the disposable_deck has been created with the correct deck
        assert disposable_deck.deck is None
        # Check if the disposable_deck has been saved in the database
        assert DisposableDeck.exists(id=0)
        # Delete the disposable_deck
        disposable_deck.delete()
        commit()
