import pytest
from pony.orm import db_session

from . import create_room
from . import create_user
from . import delete_room
from . import delete_user
from . import get_rooms
from . import join_room
from . import leave_room
from . import Room
from . import start_game


# Test suite for the room module using pytest
class TestRoom:

    # Test the room creation
    @db_session
    def test_create_room(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Check if the room has been created
        assert room is not None
        # Check if the room has been created with the correct name
        assert room.name == "test_room"
        # Check if the room has been saved in the database
        assert Room.get(name="test_room") is not None
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_create_room_already_exists(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Check if the room has been created
        assert room is not None
        # Create a room with the same user host
        with pytest.raises(PermissionError):
            create_room("test_room", user.id)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_create_room_user_not_found(self):
        # Create a room with a user that does not exist
        with pytest.raises(ValueError):
            create_room("test_room", 1)

    @db_session
    def test_create_room_user_is_in_room(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Create another room with the same user host
        with pytest.raises(PermissionError):
            create_room("test_room", user.id)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_get_rooms(self):
        # Create a user
        user = create_user("test_user")
        # Get the rooms
        rooms = get_rooms()
        # Check if the rooms are empty
        assert rooms is not None
        assert len(rooms) == 0
        # Create a room
        room = create_room("test_room", user.id)
        # Check if the room has been created
        assert room is not None
        # Get the rooms
        rooms = get_rooms()
        # Check if the rooms are not empty
        assert len(rooms) == 1
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_delete_room(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Check if the room has been created
        assert room is not None
        # Delete the room
        delete_room(room.id, user.id)
        # Check if the room has been deleted
        assert Room.get(name="test_room") is None
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_delete_room_not_found(self):
        # Delete a room that does not exist
        with pytest.raises(ValueError):
            delete_room(1, 1)

    @db_session
    def test_delete_room_user_not_found(self):
        # Delete a room with a user that does not exist
        with pytest.raises(ValueError):
            delete_room(1, 1)

    @db_session
    def test_delete_room_user_not_host(self):
        # Create a user
        user = create_user("test_user")
        user2 = create_user("test_user2")
        # Create a room
        room = create_room("test_room", user.id)
        # Delete the room with a user that is not the host
        with pytest.raises(PermissionError):
            delete_room(room.id, user2.id)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)
        delete_user(user2.id)

    @db_session
    def test_join_room(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Create a second user
        user2 = create_user("test_user2")
        # Join the room
        join_room(room.id, user2.id)
        # Check if the user has joined the room
        assert user2.room.id == room.id
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)
        delete_user(user2.id)

    @db_session
    def test_join_room_not_found(self):
        # Join a room that does not exist
        with pytest.raises(ValueError):
            join_room(1, 1)

    @db_session
    def test_join_room_user_not_found(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Join the room with a user that does not exist
        with pytest.raises(ValueError):
            join_room(room.id, 2)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_join_room_user_already_in_room(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Join the room with a user that is already in a room
        with pytest.raises(PermissionError):
            join_room(room.id, user.id)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_leave_room(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Create a second user
        user2 = create_user("test_user2")
        # Join the room
        join_room(room.id, user2.id)
        # Leave the room
        leave_room(room.id, user2.id)
        # Check if the user has left the room
        assert user2.room is None
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the users
        delete_user(user.id)
        delete_user(user2.id)

    @db_session
    def test_leave_room_not_found(self):
        # Leave a room that does not exist
        with pytest.raises(ValueError):
            leave_room(1, 1)

    @db_session
    def test_leave_room_user_not_found(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Leave the room with a user that does not exist
        with pytest.raises(ValueError):
            leave_room(room.id, 2)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_leave_room_user_not_in_room(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Leave the room with a user that is not in the room
        with pytest.raises(ValueError):
            leave_room(room.id, 2)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_leave_room_user_host(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Leave the room with the host
        leave_room(room.id, user.id)
        # Check if the room has been deleted
        assert Room.get(name="test_room") is None
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_leave_room_user_host_with_users(self):
        # Create a user
        user = create_user("test_user")
        # Create a second user
        user2 = create_user("test_user2")
        # Create a room
        room = create_room("test_room", user.id)
        # Join the room
        join_room(room.id, user2.id)
        # Leave the room with the host
        leave_room(room.id, user.id)
        # Check if the room has been deleted
        assert Room.get(name="test_room") is None
        # Delete the user
        delete_user(user.id)
        delete_user(user2.id)

    @db_session
    def test_start_game_not_found(self):
        # Start a game in a room that does not exist
        with pytest.raises(ValueError):
            start_game(1, 1)

    @db_session
    def test_start_game_user_not_found(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        with pytest.raises(ValueError):
            start_game(room.id, 2)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_start_game_user_not_host(self):
        # Create a user
        user = create_user("test_user")
        # Create a second user
        user2 = create_user("test_user2")
        # Create a room
        room = create_room("test_room", user.id)
        # Join the room
        join_room(room.id, user2.id)
        # Start the game with a user that is not the host
        with pytest.raises(PermissionError):
            start_game(room.id, user2.id)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the users
        delete_user(user.id)
        delete_user(user2.id)

    @db_session
    def test_start_game_room_full(self):
        # Create a user
        user = create_user("test_user")
        # Create a second user
        user2 = create_user("test_user2")
        # Create a third user
        user3 = create_user("test_user3")
        # Create a room
        room = create_room("test_room", user.id)
        # Join the room
        join_room(room.id, user2.id)
        # Join the room
        join_room(room.id, user3.id)
        # Start the game
        with pytest.raises(PermissionError):
            start_game(room.id, user.id)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the users
        delete_user(user.id)
        delete_user(user2.id)
        delete_user(user3.id)
