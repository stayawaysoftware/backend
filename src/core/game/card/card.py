"""Module providing the Card class."""

class Card:
    """
    Stay Away card class.

    Attributes:
        number (int): Card number in the deck.
        name (str): Card name.
        description (str): Card description.
        category (str): Card category (Action, Defense, Obstacle, Infection, Panic).

    Methods:
        Get methods:
            get_number(): Return card number.
            get_name(): Return card name.
            get_description(): Return card description.
            get_category(): Return card category.
    """
    def __init__(self, number: int, name: str, description: str, category: str):
        self.number = number
        self.name = name
        self.description = description
        self.category = category

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
