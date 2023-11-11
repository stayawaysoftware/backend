from typing import Optional

import core.game as ga


def effect_handler(
    id_game: int,
    id_card_type: int,
    attacker: int,
    target: int,
    last_chosen_card: Optional[int] = None,
    chosen_card: Optional[int] = None,
):
    match id_card_type:
        case 0:  # None
            raise ValueError("You can't play None card.")
        case 1:  # The Thing
            raise ValueError("You can't play The Thing card.")
        case 2:  # Infected
            raise ValueError("You can't play Infected card.")
        case 3:  # Flamethrower
            ga.flamethower_effect(target)
            return None
        case 4:  # Analysis
            return ga.analisis_effect(id_game, target)
        case 5:  # Axe
            print("Axe")
            return None
        case 6:  # Suspicion
            return ga.sospecha_effect(target, attacker)
        case 7:  # Determination
            print("Determination")
            return None
        case 8:  # Whisky
            return ga.whisky_effect(id_game, attacker)
        case 9:  # Change of position
            ga.cambio_de_lugar_effect(target, attacker)
            return None
        case 10:  # Watch your back
            ga.vigila_tus_espaldas_effect(id_game)
            return None
        case 11:  # Seduction
            ga.seduccion_effect(game_id=id_game)
            return None
        case 12:  # You better run
            ga.mas_vale_que_corras_effect(target, attacker)
            return None
        case 13:  # I'm fine here
            print("I'm fine here")
            return None
        case 14:  # Terrifying
            ga.aterrador_effect(target,attacker,last_chosen_card)
            return None
        case 15:  # No, thanks
            print("No, thanks")
            return None
        case 16:  # You failed
            print("You failed")
            return None
        case 17:  # No Barbecues
            print("No Barbecues")
            return None
        case 18:  # Quarantine
            print("Quarantine")
            return None
        case 19:  # Locked Door
            print("Locked Door")
            return None
        case 20:  # Revelations
            print("Revelations")
            return None
        case 21:  # Rotten ropes
            print("Rotten ropes")
            return None
        case 22:  # Get out of here
            print("Get out of here")
            return None
        case 23:  # Forgetful
            print("Forgetful")
            return None
        case 24:  # One, two...
            print("One, two...")
            return None
        case 25:  # Three, four...
            print("Three, four...")
            return None
        case 26:  # Is the party here?
            print("Is the party here?")
            return None
        case 27:  # Let it stay between us
            print("Let it stay between us")
            return None
        case 28:  # Turn and turn
            print("Turn and turn")
            return None
        case 29:  # Can't we be friends?
            print("Can't we be friends?")
            return None
        case 30:  # Blind date
            print("Blind date")
            return None
        case 31:  # Ups!
            print("Ups!")
            return None
        case 32:  # Exchange (Fictional card)
            ga.exchange_effect(target, attacker, last_chosen_card, chosen_card)
            return None
        case _:  # Invalid card
            raise ValueError("Card doesn't exists.")
