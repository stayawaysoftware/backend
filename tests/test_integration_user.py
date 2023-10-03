import pytest
from pony.orm import db_session

from . import create_room
from . import create_user
from . import delete_room
from . import delete_user
from . import get_users
from . import User


# Test suite for the user module using pytest
class TestUser:

    # Test the user creation
    @db_session
    def test_create_user(self):
        # Create a user
        user = create_user("test_user")
        # Check if the user has been created
        assert user is not None
        # Check if the user has been created with the correct username
        assert user.username == "test_user"
        # Check if the user has been saved in the database
        assert User.get(username="test_user") is not None
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_create_user_already_exists(self):
        # Create a user
        user = create_user("test_user")
        # Check if the user has been created
        assert user is not None
        # Create a user with the same username
        with pytest.raises(PermissionError):
            create_user("test_user")
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_get_users(self):
        # Get the users
        users = get_users()
        # Check if the users are empty
        assert users is not None
        assert len(users) == 0
        # Create a user
        user = create_user("test_user")
        # Check if the user has been created
        assert user is not None
        # Get the users
        users = get_users()
        # Check if the users are not empty
        assert len(users) == 1
        # Delete the user
        delete_user(user.id)

    @db_session
    def test_delete_user(self):
        # Create a user
        user = create_user("test_user")
        # Check if the user has been created
        assert user is not None
        # Delete the user
        delete_user(user.id)
        # Check if the user has been deleted
        assert User.get(username="test_user") is None

    @db_session
    def test_delete_user_not_found(self):
        # Delete a user that does not exist
        with pytest.raises(ValueError):
            delete_user(0)

    @db_session
    def test_delete_user_in_room(self):
        # Create a user
        user = create_user("test_user")
        # Create a room
        room = create_room("test_room", user.id)
        # Check if the room has been created
        assert room is not None
        # Check if the user is in the room
        assert user.room == room
        # Delete the user
        with pytest.raises(PermissionError):
            delete_user(user.id)
        # Delete the room
        delete_room(room.id, user.id)
        # Delete the user
        delete_user(user.id)
