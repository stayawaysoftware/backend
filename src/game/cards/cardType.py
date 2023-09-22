from enum import Enum


class CardType(Enum):
    """Enum for card types"""

    ACTION = 1
    DEFENSE = 2
    INFECTION = 3
    OBSTACLE = 4
    PANIC = 5
