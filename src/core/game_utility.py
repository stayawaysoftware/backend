"""Functions used to all the game operation (internal logic)."""
from typing import Optional

from core.card import relate_card_with_disposable_deck
from core.card import relate_card_with_player
from core.card import unrelate_card_with_available_deck
from core.card import unrelate_card_with_player
from core.card_creation import init_available_deck
from core.deck import create_available_deck
from core.deck import create_deck
from core.deck import create_disposable_deck
from core.deck import delete_available_deck
from core.deck import delete_deck
from core.deck import delete_disposable_deck
from core.deck import get_deck
from core.deck import get_random_card_from_available_deck
from core.deck import move_disposable_to_available_deck
from core.effects import do_effect
from core.game_action import GameAction
from models.game import Deck
from models.game import Game
from models.game import Player
from pony.orm import db_session

# ===================== BASIC GAME FUNCTIONS =====================

# Initialization of decks (start of the game)


def initialize_decks(id_game: int, quantity_players: int) -> Deck:
    """Initialize the decks of the game."""
    create_deck(id_game)
    create_available_deck(id_game)
    create_disposable_deck(id_game)

    init_available_deck(id_game, quantity_players)

    return get_deck(id_game)


# Delete decks (end of the game)


def delete_decks(id_game: int) -> None:
    """Delete the decks of the game."""
    delete_deck(id_game)
    delete_available_deck(id_game)
    delete_disposable_deck(id_game)


# ===================== GAME PHASES FUNCTIONS =====================

# DRAW phase


def draw(id_game: int, id_player: int) -> int:
    """Draw a card from the available deck."""
    with db_session:
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")
        if Game[1].current_phase != "Draw":
            raise ValueError(
                f"Game with id {id_game} is not in the Draw phase"
            )

    if len(get_deck(id_game).available_deck.cards) == 0:
        move_disposable_to_available_deck(id_game)

    card = get_random_card_from_available_deck(id_game)
    unrelate_card_with_available_deck(card.id, id_game)
    relate_card_with_player(card.id, id_player)
    return card.id


# PLAY phase


def play(
    id_game: int,
    id_player: int,
    idtype_card: int,
    idtype_card_before: Optional[int] = None,
    target: Optional[int] = None,
    card_chosen_by_player: Optional[int] = None,
    card_chosen_by_target: Optional[int] = None,
    first_play: bool = True
) -> GameAction:
    """Play a card from player hand."""
    with db_session:
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")
        if Game[id_game].current_phase not in ["Play", "Defense"]:
            raise ValueError(
                f"Game with id {id_game} is not in the Play/Defense phase"
            )
        if target is not None and not Player.exists(id=target):
            raise ValueError(f"Player with id {target} doesn't exist")
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if idtype_card not in [0, 32]:
            if len(Player[id_player].hand.select(idtype=idtype_card)) == 0:
                raise ValueError(
                    f"Player with id {id_player} has no card with idtype {idtype_card} in hand"
                )
        if card_chosen_by_player is not None:
            if (
                len(Player[id_player].hand.select(id=card_chosen_by_player))
                == 0
            ):
                raise ValueError(
                    f"Player with id {id_player} has no card with id {card_chosen_by_player} in hand"
                )
        if card_chosen_by_target is not None:
            if len(Player[target].hand.select(id=card_chosen_by_target)) == 0:
                raise ValueError(
                    f"Player with id {target} has no card with id {card_chosen_by_target} in hand"
                )

    return do_effect(
        id_game=id_game,
        id_player=id_player,
        id_card_type=idtype_card,
        id_card_type_before=idtype_card_before,
        target=target,
        card_chosen_by_player=card_chosen_by_player,
        card_chosen_by_target=card_chosen_by_target,
        first_play=first_play
    )


# DISCARD phase


def discard(id_game: int, idtype_card: int, id_player: int) -> int:
    """Discard a card from player hand."""
    with db_session:
        if not Game.exists(id=id_game):
            raise ValueError(f"Game with id {id_game} doesn't exist")
        if Game[id_game].current_phase != "Discard":
            raise ValueError(
                f"Game with id {id_game} is not in the Discard phase"
            )
        if not Player.exists(id=id_player):
            raise ValueError(f"Player with id {id_player} doesn't exist")
        if len(Player[id_player].hand) == 0:
            raise ValueError(
                f"Player with id {id_player} has no cards in hand"
            )
        if len(Player[id_player].hand.select(idtype=idtype_card)) == 0:
            raise ValueError(
                f"Player with id {id_player} has no card with idtype {idtype_card} in hand"
            )

        card = Player[id_player].hand.select(idtype=idtype_card).random(1)[0]

    unrelate_card_with_player(card.id, id_player)
    relate_card_with_disposable_deck(card.id, id_game)

    return card.id
