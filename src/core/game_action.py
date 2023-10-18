"""Module providing the interconnection between the game and the card effects."""
from enum import Enum
from typing import Optional


class ActionType(Enum):
    """Enum class for action types."""

    NOTHING = 1
    KILL = 2
    ASK_DEFENSE = 3

    def __str__(self) -> str:
        """Return string representation."""
        if self == ActionType.NOTHING:
            return "NOTHING"
        elif self == ActionType.KILL:
            return "KILL"
        elif self == ActionType.ASK_DEFENSE:
            return "ASK_DEFENSE"


class GameAction:
    """
    Game action class.

    Attributes:
        Obligatory:
            action (str): Action (Nothing, Kill).
        Optional:
            target (int): Action target (player id).
            defense_cards (list): List of defense cards.

    Methods:
        Get methods:
            get_action(): Return action.
            get_target(): Return target.
            get_defense_cards(): Return defense cards.
        Set methods:
            set_action(): Set action.
            set_target(): Set target.
            set_defense_cards(): Set defense cards.
    """

    def __init__(
        self,
        action: ActionType,
        target: Optional[int] = None,
        defense_cards: Optional[list[int]] = None,
    ):
        """Initialize class. Argument target is optional."""
        self.action = action
        self.target = target
        self.defense_cards = defense_cards

    def __str__(self) -> str:
        """Return string representation."""
        return f"Action: {self.action}, Target: {self.target}, Defense cards: {self.defense_cards}"

    def get_action(self) -> ActionType:
        """Return action."""
        return self.action

    def get_target(self) -> Optional[int]:
        """Return target."""
        return self.target

    def get_defense_cards(self) -> Optional[list[int]]:
        """Return defense cards."""
        return self.defense_cards

    def set_action(self, action: ActionType):
        """Set action."""
        self.action = action

    def set_target(self, target: Optional[int]):
        """Set target."""
        self.target = target

    def set_defense_cards(self, defense_cards: Optional[list[int]]):
        """Set defense cards."""
        self.defense_cards = defense_cards
