from pony.orm import (PrimaryKey, Required, Set, Optional)
from db import db

class User(db.Entity):
    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str, 30)
    id_lobby = Optional('Room')

class Room(db.Entity):
    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str, 30)
    id_user = Set(User)
    minimum_cnt_users = Required(int, default=4, unsigned=True)
    maximum_cnt_users = Required(int, default=12)