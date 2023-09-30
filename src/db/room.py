from db.database import db
from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Set


class User(db.Entity):
    """User entity."""

    id = PrimaryKey(int, auto=True, unsigned=True)
    username = Required(str, 30)
    lobby = Optional("Room")


class Room(db.Entity):
    """Room entity."""

    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str, 30)
    users = Set("User")
    host_id = Required(int)
    min_users = Required(int, default=4, unsigned=True)
    max_users = Required(int, default=12)
