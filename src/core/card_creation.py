"""Card creation and relationship functions for Stay Away!'s cards."""
from core.card import create_card
from core.card import relate_card_with_available_deck
from core.deck import get_available_deck
from models.game import Card
from pony.orm import db_session

# ===================== CARD DATA =====================

# Card names + category
card_names = [
    ["None", "None"],
    ["The Thing", "INFECTION"],
    ["Infected", "INFECTION"],
    ["Flamethrower", "ACTION"],
    ["Analysis", "ACTION"],
    ["Axe", "ACTION"],
    ["Suspicion", "ACTION"],
    ["Determination", "ACTION"],
    ["Whisky", "ACTION"],
    ["Change of position", "ACTION"],
    ["Watch your back", "ACTION"],
    ["Seduction", "ACTION"],
    ["You better run", "ACTION"],
    ["I'm fine here", "DEFENSE"],
    ["Terrifying", "DEFENSE"],
    ["No, thanks", "DEFENSE"],
    ["You failed", "DEFENSE"],
    ["No Barbecues", "DEFENSE"],
    ["Quarantine", "OBSTACLE"],
    ["Locked Door", "OBSTACLE"],
    ["Revelations", "PANIC"],
    ["Rotten ropes", "PANIC"],
    ["Get out of here", "PANIC"],
    ["Forgetful", "PANIC"],
    ["One, two...", "PANIC"],
    ["Three, four...", "PANIC"],
    ["Is the party here?", "PANIC"],
    ["Let it stay between us", "PANIC"],
    ["Turn and turn", "PANIC"],
    ["Can't we be friends?", "PANIC"],
    ["Blind date", "PANIC"],
    ["Ups!", "PANIC"],
]

# Cards id that defends the card

card_defense = [
    [],  # None 0 --> Fictional card
    [],  # The Thing 1
    [],  # Infected 2
    [17],  # Flamethrower 3
    [],  # Analysis 4
    [],  # Axe 5
    [],  # Suspicion 6
    [],  # Determination 7
    [],  # Whisky 8
    [13,14,15,16],  # Change of position 9
    [],  # Watch your back 10
    [14,15,16],  # Seduction 11
    [13],  # You better run 12
    [],  # I'm fine here 13
    [],  # Terrifying 14
    [],  # No, thanks 15
    [],  # You failed 16
    [],  # No Barbecues 17
    [],  # Quarantine 18
    [],  # Locked Door 19
    [],  # Revelations 20
    [],  # Rotten ropes 21
    [],  # Get out of here 22
    [],  # Forgetful 23
    [],  # One, two... 24
    [],  # Three, four... 25
    [],  # Is the party here? 26
    [],  # Let it stay between us 27
    [],  # Turn and turn 28
    [],  # Can't we be friends? 29
    [],  # Blind date 30
    [],  # Ups! 31
    [14,15,16],  # Exchange 32 --> Fictional card
]

# Quantity of cards of different category for quantity of players
quantity_cards = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # None
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # The Thing
    [0, 0, 0, 0, 8, 0, 2, 2, 1, 2, 2, 3, 0],  # Infected
    [0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 0, 1, 0],  # Flamethrower
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0],  # Analysis
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # Axe
    [0, 0, 0, 0, 4, 0, 0, 1, 1, 1, 1, 0, 0],  # Suspicion
    [0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 1, 0, 0],  # Determination
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],  # Whisky
    [0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 1, 0],  # Change of position
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # Watch your back
    [0, 0, 0, 0, 2, 0, 1, 1, 1, 0, 1, 1, 0],  # Seduction
    [0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 1, 0],  # You better run
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],  # I'm fine here
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0],  # Terrifying
    [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],  # No, thanks
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],  # You failed
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],  # No Barbecues
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # Quarantine
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],  # Locked Door
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # Revelations
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # Rotten ropes
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # Get out of here
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Forgetful
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # One, two...
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # Three, four...
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # Is the party here?
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],  # Let it stay between us
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # Turn and turn
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],  # Can't we be friends?
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # Blind date
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # Ups!
]

# ===================== INITIAL CARD FUNCTIONS =====================

# Create cards


def create_all_cards() -> None:
    """Create all cards in the database."""
    with db_session:
        if len(Card.select()) > 0:
            raise ValueError("Cards already created")

    counter = 0
    for i in range(len(card_names)):
        sum = 0
        for j in range(len(quantity_cards[i])):
            sum += quantity_cards[i][j]
        while sum > 0:
            create_card(counter, i, card_names[i][0], card_names[i][1])
            sum -= 1
            counter += 1

    assert len(Card.select()) == 109


# Initialize available deck creating relationship with cards


def init_available_deck(id_available_deck: int, quantity_players: int) -> None:
    """Initialize an available deck creating relationship with cards."""
    with db_session:
        if len(Card.select()) == 0:
            create_all_cards()

    available_deck = get_available_deck(id_available_deck)
    if len(available_deck.cards) > 0:
        raise ValueError(
            f"Available deck with id {id_available_deck} already initialized"
        )

    for i in range(len(card_names)):
        with db_session:
            card_list = list(Card.select(idtype=i))

        sum = 0
        for j in range(quantity_players + 1):
            sum += quantity_cards[i][j]

        for j in range(sum):
            relate_card_with_available_deck(card_list[j].id, id_available_deck)
