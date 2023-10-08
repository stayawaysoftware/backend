from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Set

from . import db


class Player(db.Entity):
    """Player model."""

    id = PrimaryKey(int)
    role = Required(str, default="Human")  # Human, The Thing, Infected
    name = Required(str)
    round_position = Required(int, unsigned=True)
    alive = Required(bool, default=1)
    game = Set("Game")
    hand = Set("Card")


class Game(db.Entity):
    """Game model."""

    id = PrimaryKey(int)
    round_left_direction = Required(bool, default=0)
    status = Required(str, default="In progress")
    current_phase = Required(str, default="Draw")  # Draw, Play, Discard
    current_position = Optional(int, default=1, unsigned=True)
    players = Set("Player")
    deck = Required("Deck")


class Card(db.Entity):
    """Card model."""

    id = PrimaryKey(int, auto=True, unsigned=True)
    idtype = Required(int, unsigned=True)
    name = Required(str, 30)
    type = Required(
        str, default="Action"
    )  # Action, Defense, Infection, Obstacle, Panic

    available_deck = Set("AvailableDeck", reverse="cards")
    disposable_deck = Set("DisposableDeck", reverse="cards")
    players = Set("Player")


class AvailableDeck(db.Entity):
    """AvailableDeck model."""

    id = PrimaryKey(int)
    deck = Optional("Deck")
    cards = Set("Card", reverse="available_deck")


class DisposableDeck(db.Entity):
    """DisposableDeck model."""

    id = PrimaryKey(int)
    deck = Optional("Deck")
    cards = Set("Card", reverse="disposable_deck")


class Deck(db.Entity):
    """Deck model."""

    id = PrimaryKey(int)
    available_deck = Optional("AvailableDeck")
    disposable_deck = Optional("DisposableDeck")
    game = Optional("Game")
