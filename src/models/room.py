from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Set

from . import db


class User(db.Entity):
    """User entity."""

    id = PrimaryKey(int, auto=True, unsigned=True)
    username = Required(str, 32)
    room = Optional("Room")


class Room(db.Entity):
    """Room entity."""

    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str, 32)
    users = Set("User")
    host_id = Required(int)
    in_game = Required(bool)
    min_users = Required(int, default=4, unsigned=True)
    max_users = Required(int, default=12, unsigned=True)
    pwd = Optional(str, nullable=True)
