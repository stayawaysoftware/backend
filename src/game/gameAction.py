from enum import Enum


class GameActionType(Enum):
    """Enum for game action types"""

    NOTHING = 0
    KILL = 1


class GameAction:
    """Class to represent an action of the game"""

    def __init__(
        self, action_type: GameActionType, players_affected: list[int]
    ):  # players_affected: list[id_players]
        """Constructor for GameAction class"""
        self.action_type = action_type
        self.players_affected = players_affected

    def __str__(self) -> str:
        """String representation of GameAction class"""
        return f"GameAction: {self.action_type} ({self.players_affected})"

    def get_action_type(self) -> GameActionType:
        """Return the action type"""
        return self.action_type

    def get_players_affected(self) -> list[int]:
        """Return the players affected"""
        return self.players_affected

    def set_action_type(self, action_type: GameActionType) -> None:
        """Set the action type"""
        self.action_type = action_type

    def set_players_affected(self, players_affected: list[int]) -> None:
        """Set the players affected"""
        self.players_affected = players_affected
