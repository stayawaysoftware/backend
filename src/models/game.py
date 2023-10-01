from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Set

from . import db


class Player(db.Entity):
    """Player model."""

    id = PrimaryKey(int)
    role = Required(str, default="Human")  # Human, The Thing, Infected
    round_position = Required(int, unique=True, unsigned=True)
    alive = Required(bool, default=1)

    game = Required("Game")
    hand = Required(Set("Card"))


class Game(db.Entity):
    """Game model."""

    id = PrimaryKey(int)
    round_left_direction = Required(bool, default=0)
    actual_phase = Required(str, default="Draw")  # Draw, Play, Discard
    actual_position = Optional(int, default=1, unsigned=True)

    players = Set("Player")
    deck = Required("Deck")


class Card(db.Entity):
    """Card model."""

    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str, 30)
    type = Required(
        str, default="Action"
    )  # Action, Defense, Infection, Obstacle, Panic

    decks = Optional(Set("Deck"))
    players = Optional(Set("Player"))


class Deck(db.Entity):
    """Deck model."""

    id = PrimaryKey(int)
    available_cards = Optional(Set("Card"))
    disposable_cards = Optional(Set("Card"))
