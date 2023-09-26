"""Module providing the interconnection between the game and the card effects."""
from typing import Optional


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

    def __init__(self, action: str, target: Optional[int]):
        """Initialize class. Argument target is optional."""
        self.action = action
        self.target = target

    def __str__(self) -> str:
        """Return string representation."""
        if self.target is None:
            return f"{self.action}"
        return f"{self.action} - {self.target}"

    def get_action(self) -> str:
        """Return action."""
        return self.action

    def get_target(self) -> Optional[int]:
        """Return target."""
        return self.target

    def set_action(self, action: str):
        """Set action."""
        self.action = action

    def set_target(self, target: int):
        """Set target."""
        self.target = target
