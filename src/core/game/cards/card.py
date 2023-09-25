from typing import Callable

from src.core.game.cards.card_type import CardType
from src.core.game.game import Game


class Card:
    """Class card like template for used cards in The Thing Game"""

    def __init__(
        self,
        card_id: int,
        name: str,
        description: str,
        type: CardType,
        deck_id: int,
        function_to_do_efect: Callable[[Game, list[int]], None],
    ) -> None:
        """Constructor for Card class"""
        self.card_id = card_id
        self.name = name
        self.description = description
        self.type = type
        self.deck_id = deck_id
        self.function_to_do_efect = function_to_do_efect

    def __str__(self) -> str:
        """String representation of Card class"""
        return f"Card: {self.name} ({self.card_id}) ({self.type})\
             ({self.deck_id})"

    def get_card_id(self) -> int:
        """Return the card id"""
        return self.card_id

    def get_name(self) -> str:
        """Return the card name"""
        return self.name

    def get_description(self) -> str:
        """Return the card description"""
        return self.description

    def get_type(self) -> CardType:
        """Return the card type"""
        return self.type

    def get_deck_id(self) -> int:
        """Return the deck id"""
        return self.deck_id

    def get_function_to_do_efect(self) -> Callable[[Game, list[int]], None]:
        """Return the function to do effect"""
        return self.function_to_do_efect

    def set_card_id(self, card_id: int) -> None:
        """Set the card id"""
        self.card_id = card_id

    def set_name(self, name: str) -> None:
        """Set the card name"""
        self.name = name

    def set_description(self, description: str) -> None:
        """Set the card description"""
        self.description = description

    def set_type(self, type: CardType) -> None:
        """Set the card type"""
        self.type = type

    def set_deck_id(self, deck_id: int) -> None:
        """Set the deck id"""
        self.deck_id = deck_id

    def set_function_to_do_efect(
        self, function_to_do_efect: Callable[[Game, list[int]], None]
    ) -> None:
        """Set the function to do effect"""
        self.function_to_do_efect = function_to_do_efect

    def do_effect(self, game: Game, targets: list[int] = None) -> None:
        """Do effect of card"""
        if targets is None:
            targets = []
        return self.do_effect(game, targets)
