from core.game import *

def effect_handler(id_game:int ,id_card_type: int,attacker: int,target: int):
    match id_card_type:
        case 0:  # None 
            raise ValueError("You can't play None card.")
        case 1:  # The Thing
            raise ValueError("You can't play The Thing card.")
        case 2:  # Infected
            raise ValueError("You can't play Infected card.")
        case 3:  # Flamethrower
            flamethower_effect(target)
            return None
        case 4:  # Analysis
            return analisis_effect(target)
        case 5:  # Axe
            print("Axe")
            return None
        case 6:  # Suspicion
            sospecha_effect(target, attacker)
            return None
        case 7:  # Determination
            print("Determination")
            return None
        case 8:  # Whisky
            return whisky_effect(attacker)
        case 9:  # Change of position
            cambio_de_lugar_effect(target, attacker)
            return None
        case 10:  # Watch your back
            vigila_tus_espaldas_effect(id_game)
            return None
        case 11:  # Seduction
            seduccion_effect(target, attacker)
            return None
        case 12:  # You better run
            mas_vale_que_corras_effect(target, attacker)
            return None
        case 13:  # I'm fine here
            print("I'm fine here")
            return None
        case 14:  # Terrifying
            print("Terrifying")
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
            print("Exchange")
            return None
        case _:  # Invalid card
            raise ValueError("Card doesn't exists.")