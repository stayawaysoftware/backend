"""Effects of the cards."""
from typing import Optional

from core.game_action import ActionType
from core.game_action import GameAction
from models.game import Game
from pony.orm import db_session


def do_effect(
    id_game: int, id_card_type: int, target: Optional[int] = None
) -> GameAction:
    """Do effect."""
    with db_session:
        if not Game.exists(id=id_game):
            raise ValueError("Game doesn't exists.")

    match id_card_type:
        case 1:  # The Thing
            return nothing_effect(id_game)
        case 2:  # Infected
            return nothing_effect(id_game)
        case 3:  # Flamethrower
            return flamethrower_effect(id_game, target)
        case 4:  # Analysis
            return nothing_effect(id_game)
        case 5:  # Axe
            return nothing_effect(id_game)
        case 6:  # Suspicion
            return nothing_effect(id_game)
        case 7:  # Determination
            return nothing_effect(id_game)
        case 8:  # Whisky
            return nothing_effect(id_game)
        case 9:  # Change of position
            return nothing_effect(id_game)
        case 10:  # Watch your back
            return nothing_effect(id_game)
        case 11:  # Seduction
            return nothing_effect(id_game)
        case 12:  # You better run
            return nothing_effect(id_game)
        case 13:  # I'm fine here
            return nothing_effect(id_game)
        case 14:  # Terrifying
            return nothing_effect(id_game)
        case 15:  # No, thanks
            return nothing_effect(id_game)
        case 16:  # You failed
            return nothing_effect(id_game)
        case 17:  # No Barbecues
            return nothing_effect(id_game)
        case 18:  # Quarantine
            return nothing_effect(id_game)
        case 19:  # Locked Door
            return nothing_effect(id_game)
        case 20:  # Revelations
            return nothing_effect(id_game)
        case 21:  # Rotten ropes
            return nothing_effect(id_game)
        case 22:  # Get out of here
            return nothing_effect(id_game)
        case 23:  # Forgetful
            return nothing_effect(id_game)
        case 24:  # One, two...
            return nothing_effect(id_game)
        case 25:  # Three, four...
            return nothing_effect(id_game)
        case 26:  # Is the party here?
            return nothing_effect(id_game)
        case 27:  # Let it stay between us
            return nothing_effect(id_game)
        case 28:  # Turn and turn
            return nothing_effect(id_game)
        case 29:  # Can't we be friends?
            return nothing_effect(id_game)
        case 30:  # Blind date
            return nothing_effect(id_game)
        case 31:  # Ups!
            return nothing_effect(id_game)
        case _:  # Invalid card
            raise ValueError("Card doesn't exists.")


def nothing_effect(id_game: int) -> GameAction:
    """Nothing effect."""
    with db_session:
        game = Game[id_game]

        if game.actual_phase != "Play":
            raise ValueError("You can't use this card in this phase.")

        return GameAction(ActionType.NOTHING)


def flamethrower_effect(id_game: int, target: Optional[int]) -> GameAction:
    """Flamethrower effect."""
    with db_session:
        game = Game[id_game]

        if game.actual_phase != "Play":
            raise ValueError("You can't use this card in this phase.")
        if target is None:
            raise ValueError("You must select a target.")
        if game.players.select(id=target).count() == 0:
            raise ValueError("Target doesn't exists.")
        if not game.players.select(id=target).first().alive:
            raise ValueError("Target is dead.")

        return GameAction(ActionType.KILL, target)
