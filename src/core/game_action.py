"""Module providing the interconnection between the game and the card effects."""
from enum import Enum
from typing import Optional


class ActionType(Enum):
    """Enum class for action types."""

    NOTHING = 1
    ASK_DEFENSE = 2
    ASK_EXCHANGE = 3

    EXCHANGE = 4
    INFECT = 5
    KILL = 6
    SHOW = 7
    SHOW_ALL = 8
    SHOW_ALL_TO_ALL = 9
    REVERSE_ORDER = 10
    CHANGE_POSITION = 11

    def __str__(self) -> str:
        """Return string representation."""
        if self == ActionType.NOTHING:
            return "NOTHING"
        elif self == ActionType.ASK_DEFENSE:
            return "ASK_DEFENSE"
        elif self == ActionType.ASK_EXCHANGE:
            return "ASK_EXCHANGE"
        elif self == ActionType.EXCHANGE:
            return "EXCHANGE"
        elif self == ActionType.INFECT:
            return "INFECT"
        elif self == ActionType.KILL:
            return "KILL"
        elif self == ActionType.SHOW:
            return "SHOW"
        elif self == ActionType.SHOW_ALL:
            return "SHOW_ALL"
        elif self == ActionType.SHOW_ALL_TO_ALL:
            return "SHOW_ALL_TO_ALL"
        elif self == ActionType.REVERSE_ORDER:
            return "REVERSE_ORDER"
        elif self == ActionType.CHANGE_POSITION:
            return "CHANGE_POSITION"


class GameAction:
    """
    Game action class.

    Attributes:
        Obligatory:
            action (str): Action (Nothing, Kill).
            action2 (str): Action (Infect).
        Optional:
            target (list): Action targets (player ids).
            defense_cards (list): List of defense cards.
            card_target (list): List of cards.

    Methods:
        Get methods:
            get_action(): Return action.
            get_action2(): Return action2.
            get_target(): Return targets.
            get_defense_cards(): Return defense cards.
            get_card_target(): Return cards target.
        Set methods:
            set_action(): Set action.
            set_target(): Set targets.
            set_defense_cards(): Set defense cards.
            set_card_target(): Set cards target.
    """

    def __init__(
        self,
        action: ActionType,
        action2: Optional[ActionType] = None,
        target: Optional[list[int]] = None,
        defense_cards: Optional[list[int]] = None,
        card_target: Optional[list[int]] = None,
    ):
        """Initialize class. Argument target is optional."""
        self.action = action
        self.action2 = action2
        self.target = target
        self.defense_cards = defense_cards
        self.card_target = card_target

    def __str__(self) -> str:
        """Return string representation."""
        return f"Action: {self.action}, Action2: {self.action2}, Target: {self.target}, Defense cards: {self.defense_cards}, Card target: {self.card_target}"

    def get_action(self) -> ActionType:
        """Return action."""
        return self.action

    def get_action2(self) -> Optional[ActionType]:
        """Return action2."""
        return self.action2

    def get_target(self) -> Optional[list[int]]:
        """Return target."""
        return self.target

    def get_defense_cards(self) -> Optional[list[int]]:
        """Return defense cards."""
        return self.defense_cards

    def get_card_target(self) -> Optional[list[int]]:
        """Return cards target."""
        return self.card_target

    def set_action(self, action: ActionType):
        """Set action."""
        self.action = action

    def set_action2(self, action2: Optional[ActionType]):
        """Set action2."""
        self.action2 = action2

    def set_target(self, target: Optional[list[int]]):
        """Set target."""
        self.target = target

    def set_defense_cards(self, defense_cards: Optional[list[int]]):
        """Set defense cards."""
        self.defense_cards = defense_cards

    def set_card_target(self, card_target: Optional[list[int]]):
        """Set cards target."""
        self.card_target = card_target
