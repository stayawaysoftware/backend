from pony.orm import (PrimaryKey, Required, Set, Optional)
from db import db

class Room(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    maxplayers = Required(int)
    minplayers = Required(int)
    current_players = Required(int)
    password = Optional(str)