"""Effect handler"""
from typing import Optional

from core.game_logic.card_creation import card_defense
from core.game_logic.effects.analysis_effect import analysis_effect
from core.game_logic.effects.change_of_position_effect import (
    change_of_position_effect,
)
from core.game_logic.effects.change_of_position_effect import (
    im_fine_here_effect,
)
from core.game_logic.effects.exchange_effect import exchange_effect
from core.game_logic.effects.exchange_effect import no_thanks_effect
from core.game_logic.effects.exchange_effect import terrifying_effect
from core.game_logic.effects.exchange_effect import you_failed_effect
from core.game_logic.effects.flamethrower_effect import flamethrower_effect
from core.game_logic.effects.flamethrower_effect import no_barbecues_effect
from core.game_logic.effects.nothing_effect import nothing_effect
from core.game_logic.effects.suspicion_effect import suspicion_effect
from core.game_logic.effects.watch_your_back_effect import (
    watch_your_back_effect,
)
from core.game_logic.effects.whisky_effect import whisky_effect
from core.game_logic.game_action import ActionType
from core.game_logic.game_action import GameAction
from models.game import Game
from pony.orm import db_session


def do_effect(
    id_game: int,
    id_player: int,
    id_card_type: int,
    target: Optional[int] = None,
    id_card_type_before: Optional[int] = None,
    card_chosen_by_player: Optional[int] = None,
    card_chosen_by_target: Optional[int] = None,
    first_play: bool = True,
) -> GameAction:
    """Do effect."""
    with db_session:
        if not Game.exists(id=id_game):
            raise ValueError("Game doesn't exists.")
        if not Game[id_game].players.select(id=id_player).exists():
            raise ValueError("Player doesn't exists.")

    match id_card_type:
        case 0:  # None --> Without defense (Fictional card)
            return without_defense_effect(
                id_game,
                id_player,
                target,
                id_card_type_before,
                card_chosen_by_player,
                card_chosen_by_target,
            )
        case 1:  # The Thing
            raise ValueError("You can't play The Thing card.")
        case 2:  # Infected
            raise ValueError("You can't play Infected card.")
        case 3:  # Flamethrower
            if first_play:
                return ask_defense_effect(id_card_type, target)
            else:
                return flamethrower_effect(id_game, target)
        case 4:  # Analysis
            return analysis_effect(id_game, id_player, target)
        case 5:  # Axe
            return nothing_effect(id_game)
        case 6:  # Suspicion
            return suspicion_effect(
                id_game, id_player, target, card_chosen_by_player
            )
        case 7:  # Determination
            return nothing_effect(id_game)
        case 8:  # Whisky
            return whisky_effect(id_game, id_player)
        case 9:  # Change of position
            if first_play:
                return ask_defense_effect(id_card_type, target)
            else:
                return change_of_position_effect(id_game, id_player, target)
        case 10:  # Watch your back
            return watch_your_back_effect(id_game, id_player)
        case 11:  # Seduction
            if first_play:
                return ask_defense_effect(id_card_type, target)
            else:
                return exchange_effect(
                    id_game,
                    id_player,
                    target,
                    card_chosen_by_player,
                    card_chosen_by_target,
                )
        case 12:  # You better run
            if first_play:
                return ask_defense_effect(id_card_type, target)
            else:
                return change_of_position_effect(id_game, id_player, target)
        case 13:  # I'm fine here
            return im_fine_here_effect(id_game)
        case 14:  # Terrifying
            return terrifying_effect(
                id_game, id_player, target, card_chosen_by_target
            )
        case 15:  # No, thanks
            return no_thanks_effect(id_game)
        case 16:  # You failed
            return you_failed_effect(
                id_game, id_player, target, card_chosen_by_target
            )
        case 17:  # No Barbecues
            return no_barbecues_effect(id_game)
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
        case 32:  # Exchange (Fictional card)
            if first_play:
                return ask_defense_effect(id_card_type, target)
            else:
                return exchange_effect(
                    id_game,
                    id_player,
                    target,
                    card_chosen_by_player,
                    card_chosen_by_target,
                )
        case _:  # Invalid card
            raise ValueError("Card doesn't exists.")


def without_defense_effect(
    id_game: int,
    id_player: int,
    target: Optional[int],
    id_card_type_before: Optional[int],
    card_chosen_by_player: Optional[int],
    card_chosen_by_target: Optional[int],
) -> GameAction:
    """Without defense effect."""
    with db_session:
        game = Game[id_game]

        if game.current_phase != "Defense":
            raise ValueError("You can't use this card in this phase.")
        if target is None:
            raise ValueError("You must select a target.")
        if game.players.select(id=target).count() == 0:
            raise ValueError("Target doesn't exists.")
        if not game.players.select(id=target).first().alive:
            raise ValueError("Target is dead.")
        if game.players.select(id=id_player).count() == 0:
            raise ValueError("Player doesn't exists.")
        if game.players.select(id=id_player).first().id == target:
            raise ValueError("You can't use this card on yourself.")
        if id_card_type_before is None:
            raise ValueError("You must select a card before.")

        return do_effect(
            id_game=id_game,
            id_player=target,
            id_card_type=id_card_type_before,
            target=id_player,
            card_chosen_by_player=card_chosen_by_target,
            card_chosen_by_target=card_chosen_by_player,
            first_play=False,
        )


def ask_defense_effect(id_card_type: int, target: Optional[int]) -> GameAction:
    """Ask defense effect."""
    with db_session:
        if target is None:
            raise ValueError("You must select a target.")

        return GameAction(
            action=ActionType.ASK_DEFENSE,
            target=[target],
            defense_cards=card_defense[id_card_type],
        )
