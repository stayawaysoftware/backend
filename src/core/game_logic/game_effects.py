"""Function of play phase."""
from typing import Optional

from core.game_logic.effects.effect_handler import do_effect
from core.game_logic.game_action import GameAction
from models.game import Game
from models.game import Player
from pony.orm import db_session


def play(
    id_game: int,
    id_player: int,
    idtype_card: int,
    idtype_card_before: Optional[int] = None,
    target: Optional[int] = None,
    card_chosen_by_player: Optional[int] = None,
    card_chosen_by_target: Optional[int] = None,
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
    )
