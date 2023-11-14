"""Effect handler"""
from typing import Optional

from core.game_logic.effects.analysis_effect import analysis_effect
from core.game_logic.effects.change_of_position_effect import (
    change_of_position_effect,
)
from core.game_logic.effects.change_of_position_effect import (
    im_fine_here_effect,
)
from core.game_logic.effects.change_of_position_effect import (
    you_better_run_effect,
)
from core.game_logic.effects.exchange_effect import exchange_effect
from core.game_logic.effects.exchange_effect import no_thanks_effect
from core.game_logic.effects.exchange_effect import terrifying_effect
from core.game_logic.effects.flamethrower_effect import flamethrower_effect
from core.game_logic.effects.flamethrower_effect import no_barbecues_effect
from core.game_logic.effects.suspicion_effect import suspicion_effect
from core.game_logic.effects.watch_your_back_effect import (
    watch_your_back_effect,
)
from core.game_logic.effects.whisky_effect import whisky_effect
from pony.orm import db_session

# Import effect functions


@db_session
def do_effect_attack(
    id_game: int,
    attack_player_id: int,
    defense_player_id: int,
    idtype_attack_card: int,
    card_chosen_by_attacker: Optional[int] = None,
    card_chosen_by_defender: Optional[int] = None,
):
    """Do the effect of the attack card."""

    # We want to view only the possible attack cases:

    match idtype_attack_card:
        case 3:
            # Flamethrower
            return flamethrower_effect(
                id_game=id_game,
                attack_player_id=attack_player_id,
                defense_player_id=defense_player_id,
            )
        case 4:
            # Analysis
            return analysis_effect(
                id_game=id_game,
                attack_player_id=attack_player_id,
                defense_player_id=defense_player_id,
            )
        case 5:
            # Axe
            return None
        case 6:
            # Suspicion
            return suspicion_effect(
                id_game=id_game,
                attack_player_id=attack_player_id,
                defense_player_id=defense_player_id,
            )
        case 7:
            # Determination
            return None
        case 8:
            # Whisky
            return whisky_effect(
                id_game=id_game,
                attack_player_id=attack_player_id,
            )
        case 9:
            # Change of position
            return change_of_position_effect(
                id_game=id_game,
                attack_player_id=attack_player_id,
                defense_player_id=defense_player_id,
            )
        case 10:
            # Watch your back
            return watch_your_back_effect(id_game=id_game)
        case 11:
            # Seduction
            return None
        case 12:
            # You better run
            return you_better_run_effect(
                id_game=id_game,
                attack_player_id=attack_player_id,
                defense_player_id=defense_player_id,
            )
        case 18:
            # Quarantine
            return None
        case 19:
            # Locked Door
            return None
        case 20:
            # Revelations
            return None
        case 21:
            # Rotten ropes
            return None
        case 22:
            # Get out of here
            return None
        case 23:
            # Forgetful
            return None
        case 24:
            # One, two...
            return None
        case 25:
            # Three, four...
            return None
        case 26:
            # Is the party here?
            return None
        case 27:
            # Let it stay between us
            return None
        case 28:
            # Turn and turn
            return None
        case 29:
            # Can't we be friends?
            return None
        case 30:
            # Blind date
            return None
        case 31:
            # Ups!
            return None
        case 32:
            # Exchange
            return exchange_effect(
                id_game=id_game,
                attack_player_id=attack_player_id,
                defense_player_id=defense_player_id,
                card_chosen_by_attacker=card_chosen_by_attacker,
                card_chosen_by_defender=card_chosen_by_defender,
            )
        case _:
            # The card is not an attack card. If do_effect is called, it means that the card is an attack card.
            # So, this never happens.
            raise ValueError(
                f"Card with idtype {idtype_attack_card} is not an attack card"
            )


@db_session
def do_effect_defense(
    id_game: int,
    attack_player_id: int,
    defense_player_id: int,
    idtype_attack_card: int,
    idtype_defense_card: int,
    card_chosen_by_attacker: Optional[int] = None,
    card_chosen_by_defender: Optional[int] = None,
):
    """Do the effect of the combination of cards between attacker and defender players."""

    # We want to view only the possible defense cases:

    match idtype_defense_card:
        case 0:
            # Without defense
            return do_effect_attack(
                id_game=id_game,
                attack_player_id=attack_player_id,
                defense_player_id=defense_player_id,
                idtype_attack_card=idtype_attack_card,
                card_chosen_by_attacker=card_chosen_by_attacker,
                card_chosen_by_defender=card_chosen_by_defender,
            )
        case 13:
            # I'm fine here
            return im_fine_here_effect(defense_player_id)
        case 14:
            # Terrifying
            return terrifying_effect(
                id_game,
                attack_player_id,
                defense_player_id,
                card_chosen_by_attacker,
            )
        case 15:
            # No, thanks
            return no_thanks_effect(defense_player_id)
        case 16:
            # You failed
            return None
        case 17:
            # No Barbecues
            return no_barbecues_effect(defense_player_id)
        case _:
            # The card is not a defense card. If do_effect is called, it means that the card is in the defense list of the attack card.
            # So, this never happens.
            raise ValueError(
                f"Card with idtype {idtype_defense_card} is not a defense card"
            )
