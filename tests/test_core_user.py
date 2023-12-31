import pytest
from pony.orm import db_session

from . import clean_db
from . import create_room
from . import create_user
from . import delete_room
from . import delete_user
from . import User


# Test suite for the user module using pytest
class TestUser:
    @pytest.fixture()
    @db_session
    def test_user(self):
        # Create a user for the tests
        user = create_user("test_user")
        yield user
        # Delete the user
        delete_user(user.id)

    @classmethod
    def setup_class(cls):
        clean_db()

    @classmethod
    def teardown_class(cls):
        clean_db()

    # Test the user creation
    @db_session
    def test_create_user(self, test_user):
        # Check if the user was created
        assert test_user is not None
        # Check if the user has been created with the correct username
        assert test_user.username == "test_user"
        # Check if the user has been saved in the database
        assert User.get(username="test_user") is not None

    @db_session
    def test_create_user_already_exists(self, test_user):
        # Create a user with the same username
        with pytest.raises(PermissionError):
            create_user("test_user")

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
        # Create a user to be the host
        host = create_user("test_host")
        # Use the host to create a room
        room_id = create_room("test_room", host.id)
        # Check if the user is in the room
        assert host.room is not None
        assert host.room.id == room_id
        # Delete the user
        with pytest.raises(PermissionError):
            delete_user(host.id)
        # Delete the room
        delete_room(room_id, host.id)
        # Delete the host user
        delete_user(host.id)
