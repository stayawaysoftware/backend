import pytest
from pony.orm import db_session

from . import create_room
from . import create_user
from . import db
from . import delete_room
from . import delete_user
from . import get_rooms
from . import join_room
from . import leave_room
from . import Room
from . import start_game
from . import User


# Create the needed constants for the tests
ROOM_NAME = "test_room"
USER_NAME = "test_user"
NOT_EXISTS_ID = 50


class TestRoom:
    @pytest.fixture()
    @db_session
    def resources(self):
        # Create a user for the tests
        user = create_user("test_user")
        # Create a room for the tests
        room = create_room("test_room", user.id)
        yield user, room
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @classmethod
    def tearDownClass(cls):
        db.drop_all_tables(with_all_data=True)

    # Test the room creation
    @db_session
    def test_create_room(self, resources):
        room = resources[1]
        # Check if the room has been created
        assert room is not None
        # Check if the room has been created with the correct name
        assert room.name == "test_room"
        # Check if the room has been saved in the database
        assert Room.get(name="test_room") is not None

    @db_session
    def test_create_room_user_not_found(self):
        # Assert not exists user with id 1
        assert User.get(id=NOT_EXISTS_ID) is None
        # Create a room with a user that does not exist
        with pytest.raises(ValueError):
            create_room("test_room", NOT_EXISTS_ID)

    @db_session
    def test_create_room_user_is_in_room(self, resources):
        user = resources[0]
        room = resources[1]
        # Assert user is in room
        assert user.room.id == room.id
        # Create another room with the same user host
        with pytest.raises(PermissionError):
            create_room("test_room", user.id)

    @db_session
    def test_get_rooms(self, resources):
        # Create a user
        temp_user = create_user("temp_user")
        # Get the rooms
        rooms = get_rooms()
        # Check if the rooms are empty
        assert rooms is not None
        assert len(rooms) == 1
        # Create a temporal room
        room = create_room("test_temporal_room", temp_user.id)
        # Get the rooms
        rooms = get_rooms()
        # Check if the rooms have the room created
        assert len(rooms) == 2
        # Delete the temporal room
        delete_room(room.id, temp_user.id)
        # Delete the user
        delete_user(temp_user.id)

    @db_session
    def test_delete_room(self):
        temp_user = create_user("temp_user")
        # Create a temporal room
        room = create_room("test_temporal_room", temp_user.id)
        # Check if the room has been created
        assert room is not None
        # Check if the room have the user as host
        assert room.id == temp_user.room.id
        # Delete the room
        delete_room(room.id, temp_user.id)
        # Check if the room has been deleted
        assert Room.get(name="test_temporal_room") is None
        # Delete the user
        delete_user(temp_user.id)

    @db_session
    def test_delete_room_not_found(self):
        # Delete a room that does not exist
        with pytest.raises(ValueError):
            delete_room(NOT_EXISTS_ID, 1)

    @db_session
    def test_delete_room_user_not_found(self):
        # Delete a room with a user that does not exist
        with pytest.raises(ValueError):
            delete_room(1, NOT_EXISTS_ID)

    @db_session
    def test_delete_room_user_not_host(self, resources):
        # Get the resources
        room = resources[1]
        # Create a user
        temp_user = create_user("temp_user")
        # Delete the room with a user that is not the host
        with pytest.raises(PermissionError):
            delete_room(room.id, temp_user.id)
        # Delete the user
        delete_user(temp_user.id)

    @db_session
    def test_join_room(self):
        # Create temp users and room
        temp_user = create_user("temp_user")
        room = create_room("test_temporal_room", temp_user.id)
        # Check if the user has joined the room
        assert room.users.count() == 1
        temp_user2 = create_user("temp_user2")
        # Join the room
        join_room(room.id, temp_user2.id)
        # Check if the user has joined the room
        assert room.users.count() == 2
        # Delete the room
        delete_room(room.id, temp_user.id)
        # Delete the users
        delete_user(temp_user.id)
        delete_user(temp_user2.id)

    @db_session
    def test_join_room_not_found(self):
        # Join a room that does not exist
        with pytest.raises(ValueError):
            join_room(NOT_EXISTS_ID, 1)

    @db_session
    def test_join_room_user_not_found(self):
        # Join the room with a user that does not exist
        with pytest.raises(ValueError):
            join_room(1, NOT_EXISTS_ID)

    @db_session
    def test_join_room_user_already_in_room(self, resources):
        # Get the resources
        room = resources[1]
        user = resources[0]
        # Join the room with a user that is already in a room
        with pytest.raises(PermissionError):
            join_room(room.id, user.id)

    @db_session
    def test_leave_room(self, resources):
        # Get the resources
        room = resources[1]
        # Create a second user
        temp_user = create_user("temp_user")
        # Join the room
        join_room(room.id, temp_user.id)
        # Leave the room
        leave_room(room.id, temp_user.id)
        # Check if the user has left the room
        assert temp_user.room is None
        # Delete the user
        delete_user(temp_user.id)

    @db_session
    def test_leave_room_not_found(self):
        # Leave a room that does not exist
        with pytest.raises(ValueError):
            leave_room(NOT_EXISTS_ID, 1)

    @db_session
    def test_leave_room_user_not_found(self, resources):
        # Get the resources
        room = resources[1]
        # Leave the room with a user that does not exist
        with pytest.raises(ValueError):
            leave_room(room.id, NOT_EXISTS_ID)

    @db_session
    def test_leave_room_user_not_in_room(self, resources):
        # Get the resources
        room = resources[1]
        # Create a temp user
        temp_user = create_user("temp_user")
        # Leave the room with a user that is not in the room
        with pytest.raises(PermissionError):
            leave_room(room.id, temp_user.id)
        # Delete the user
        delete_user(temp_user.id)

    @db_session
    def test_leave_room_user_host(self):
        # Create a temp user and room
        temp_user = create_user("temp_user")
        temp_room = create_room("temp_room", temp_user.id)
        # Leave the room with the host
        leave_room(temp_room.id, temp_user.id)
        # Check if the room has been deleted
        assert Room.get(name="test_room") is None
        # Delete the user
        delete_user(temp_user.id)

    @db_session
    def test_leave_room_user_host_with_users(self):
        # Create a user
        temp_user = create_user("temp_user")
        # Create a second user
        temp_user2 = create_user("temp_user2")
        # Create a room
        room = create_room("test_room", temp_user.id)
        # Join the room
        join_room(room.id, temp_user2.id)
        # Leave the room with the host
        leave_room(room.id, temp_user.id)
        # Check if the room has been deleted
        assert Room.get(name="test_room") is None
        # Delete the user
        delete_user(temp_user.id)
        delete_user(temp_user2.id)

    @db_session
    def test_start_game_not_found(self, resources):
        # Get the resources
        user = resources[0]
        # Start a game in a room that does not exist
        with pytest.raises(ValueError):
            start_game(NOT_EXISTS_ID, user.id)

    @db_session
    def test_start_game_user_not_found(self, resources):
        # Create a room
        room = resources[1]
        with pytest.raises(ValueError):
            start_game(room.id, NOT_EXISTS_ID)

    @db_session
    def test_start_game_user_not_host(self):
        # Create a user
        temp_user = create_user("temp_user")
        # Create a second user
        temp_user2 = create_user("temp_user2")
        # Create a room
        temp_room = create_room("temp_room", temp_user.id)
        # Join the room
        join_room(temp_room.id, temp_user2.id)
        # Start the game with a user that is not the host
        with pytest.raises(PermissionError):
            start_game(temp_room.id, temp_user2.id)
        # Delete the room
        delete_room(temp_room.id, temp_user.id)
        # Delete the users
        delete_user(temp_user.id)
        delete_user(temp_user2.id)

    @db_session
    def test_start_game_room_full(self):
        # Create a user
        temp_user = create_user("temp_user")
        # Create a second user
        temp_user2 = create_user("temp_user2")
        # Create a third user
        temp_user3 = create_user("temp_user3")
        # Create a room
        room = create_room("test_room", temp_user.id)
        # Join the room
        join_room(room.id, temp_user2.id)
        # Join the room
        join_room(room.id, temp_user3.id)
        # Start the game
        with pytest.raises(PermissionError):
            start_game(room.id, temp_user.id)
        # Delete the room
        delete_room(room.id, temp_user.id)
        # Delete the users
        delete_user(temp_user.id)
        delete_user(temp_user2.id)
        delete_user(temp_user3.id)
