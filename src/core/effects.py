"""Effects of the cards."""
from typing import Optional

from core.card_creation import card_defense
from core.game_action import ActionType
from core.game_action import GameAction
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


def nothing_effect(id_game: int) -> GameAction:
    """Nothing effect."""
    with db_session:
        return GameAction(action=ActionType.NOTHING)


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


def flamethrower_effect(id_game: int, target: Optional[int]) -> GameAction:
    """Flamethrower effect."""
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

        return GameAction(action=ActionType.KILL, target=[target])


def exchange_effect(
    id_game: int,
    player: int,
    target: Optional[int],
    card_chosen_by_player: Optional[int],
    card_chosen_by_target: Optional[int],
) -> GameAction:
    """Exchange effect."""
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
        if game.players.select(id=player).count() == 0:
            raise ValueError("Player doesn't exists.")
        if game.players.select(id=player).first().id == target:
            raise ValueError("You can't use this card on yourself.")
        if card_chosen_by_player is None:
            raise ValueError("You must select a card before.")
        if card_chosen_by_target is None:
            raise ValueError("You must select a card before.")

        player_infected = None

        player_role = game.players.select(id=player).first().role
        target_role = game.players.select(id=target).first().role

        player_hand = list(game.players.select(id=player).first().hand)
        target_hand = list(game.players.select(id=target).first().hand)

        player_cnt_infected_cards = 0
        target_cnt_infected_cards = 0

        for card in player_hand:
            if card.idtype == 2:
                player_cnt_infected_cards += 1

        for card in target_hand:
            if card.idtype == 2:
                target_cnt_infected_cards += 1

        if card_chosen_by_player == 1 or card_chosen_by_target == 1:
            raise ValueError("You can't exchange The Thing card.")

        if card_chosen_by_player == 2 and card_chosen_by_target == 2:
            raise ValueError(
                "You can't exchange Infected card from both sides."
            )

        elif card_chosen_by_player == 2:
            if player_role == "The Thing":
                if target_role == "Infected":
                    raise ValueError(
                        f"Player with id {player} can't exchange Infected card with another Infected player."
                    )

                elif target_role == "Human":
                    player_infected = target

            elif player_role == "Infected":
                if player_cnt_infected_cards == 1:
                    raise ValueError(
                        f"Player with id {player} can't exchange Infected card because he has only one Infected card."
                    )

                if target_role == "The Thing":
                    pass  # Nothing to do

                elif target_role == "Infected" or target_role == "Human":
                    raise ValueError(
                        f"Player with id {player} can't exchange Infected card with another Infected or Human player."
                    )

            elif player_role == "Human":
                raise ValueError(
                    f"Player with id {player} can't exchange Infected card because he's an human."
                )

        elif card_chosen_by_target == 2:
            if target_role == "The Thing":
                if player_role == "Infected":
                    raise ValueError(
                        f"Player with id {target} can't exchange Infected card with another Infected player."
                    )

                elif player_role == "Human":
                    player_infected = player

            elif target_role == "Infected":
                if target_cnt_infected_cards == 1:
                    raise ValueError(
                        f"Player with id {target} can't exchange Infected card because he has only one Infected card."
                    )

                if player_role == "The Thing":
                    pass

                elif player_role == "Infected" or player_role == "Human":
                    raise ValueError(
                        f"Player with id {target} can't exchange Infected card with another Infected or Human player."
                    )

            elif target_role == "Human":
                raise ValueError(
                    f"Player with id {target} can't exchange Infected card because he's an human."
                )

        if player_infected is None:
            return GameAction(
                action=ActionType.EXCHANGE,
                target=[player, target],
                card_target=[card_chosen_by_player, card_chosen_by_target],
            )
        else:
            return GameAction(
                action=ActionType.EXCHANGE,
                action2=ActionType.INFECT,
                target=[player, target, player_infected],
                card_target=[card_chosen_by_player, card_chosen_by_target],
            )
