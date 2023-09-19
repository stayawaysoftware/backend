from pony.orm import (PrimaryKey, Required, Set, Optional)
from .room import Room, User
from db import db

class Game(Room):
    round_left_direction = Required(bool, default=0)
    actual_phase = Required(str, default='Draw')  # Draw, Play, Discard
    actual_position = Optional(int, default=1, unsigned=True)
    decks = Set('Deck')


class Player(User):
    role = Required(str, default='Human')  # Human, The Thing, Infected
    round_position = Required(int, unique=True, unsigned=True)
    alive = Required(bool, default=1)

class Card(db.Entity):
    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str, 30)
    description = Required(str, 100)
    type = Required(str, default='Action')  # Action, Defense, Infection, Obstacle, Panic
    decks = Set('Deck')

class Deck(db.Entity):
    games = Required(Game)
    cards = Required(Card)
    is_available_deck = Required(bool)
    PrimaryKey(games, cards)

