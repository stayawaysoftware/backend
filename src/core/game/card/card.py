"""Module providing the Card class."""
from typing import Callable
from typing import Optional

from src.core.game.game import Game
from src.core.game.game_action import GameAction


class Card:
    """
    Stay Away card class.

    Attributes:
        number (int): Card number in the deck.
        name (str): Card name.
        description (str): Card description.
        category (str): Card category (Action, Defense, Obstacle, Infection, Panic).
        effect (Callable[[Game, Optional[int]], GameAction]): Card effect.
            Card function that takes a game and returns a game action, calculating the card effect in this game.

    Methods:
        Get methods:
            get_number(): Return card number.
            get_name(): Return card name.
            get_description(): Return card description.
            get_category(): Return card category.
        Other methods:
            do_effect(): Return card effect in this game (GameAction).
    """

    def __init__(
        self,
        number: int,
        name: str,
        description: str,
        category: str,
        effect: Callable[[Game, Optional[int]], GameAction],
    ):
        """Initialize class."""
        self.number = number
        self.name = name
        self.description = description
        self.category = category
        self.effect = effect

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.number} - {self.category} - {self.name}"

    def get_number(self) -> int:
        """Return card number."""
        return self.number

    def get_name(self) -> str:
        """Return card name."""
        return self.name

    def get_description(self) -> str:
        """Return card description."""
        return self.description

    def get_category(self) -> str:
        """Return card category."""
        return self.category

    def do_effect(self, game: Game, target: Optional[int]) -> GameAction:
        """Return card effect in this game."""
        return self.effect(game, target)
