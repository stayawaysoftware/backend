"""Module providing the interconnection between the game and the card effects."""
from enum import Enum
from typing import Optional


class ActionType(Enum):
    """Enum class for action types."""

    NOTHING = 1
    KILL = 2

    def __str__(self) -> str:
        """Return string representation."""
        if self == ActionType.NOTHING:
            return "Nothing"
        elif self == ActionType.KILL:
            return "Kill"


class GameAction:
    """
    Game action class.

    Attributes:
        Obligatory:
            action (str): Action (Nothing, Kill).
        Optional:
            target (int): Action target (player id).

    Methods:
        Get methods:
            get_action(): Return action.
            get_target(): Return target.
        Set methods:
            set_action(): Set action.
            set_target(): Set target.
    """

    def __init__(self, action: ActionType, target: Optional[int] = None):
        """Initialize class. Argument target is optional."""
        self.action = action
        self.target = target

    def __str__(self) -> str:
        """Return string representation."""
        if self.target is None:
            return str(self.action)
        return str(self.action) + " - " + str(self.target)

    def get_action(self) -> ActionType:
        """Return action."""
        return self.action

    def get_target(self) -> Optional[int]:
        """Return target."""
        return self.target

    def set_action(self, action: ActionType):
        """Set action."""
        self.action = action

    def set_target(self, target: Optional[int]):
        """Set target."""
        self.target = target
