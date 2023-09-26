from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Set

from . import db


class User(db.Entity):
    id = PrimaryKey(int, auto=True, unsigned=True)
    username = Required(str, 30)
    id_lobby = Optional("Room")


class Room(db.Entity):
    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str, 30)
    id_user = Set(User)
    minimum_cnt_users = Required(int, default=4, unsigned=True)
    maximum_cnt_users = Required(int, default=12)
