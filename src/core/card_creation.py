"""Card creation and asociation module for Stay Away cards."""
from card import add_available_deck_to_card
from card import create_card
from models.game import AvailableDeck
from models.game import Card

# Card names
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

# Cnt card of different type for cnt of players
cnt_cards = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # None
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # The Thing
    [0, 0, 0, 0, 8, 0, 2, 2, 1, 2, 2, 3, 0],  # Infected
    [0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 0, 1, 0],  # Flamethrower
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],  # Analysis
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # Axe
    [0, 0, 0, 0, 4, 0, 0, 1, 1, 0, 1, 0, 0],  # Suspicion
    [0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 1, 0, 0],  # Determination
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],  # Whisky
    [0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 1, 0],  # Change of position
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # Watch your back
    [0, 0, 0, 0, 2, 0, 1, 1, 1, 0, 1, 1, 0],  # Seduction
    [0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 1, 0],  # You better run
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],  # I'm fine here
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0],  # Terrifying
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],  # No, thanks
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],  # You failed
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],  # No Barbecues
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # Quarantine
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # Locked Door
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


def create_all_cards():
    """Create all cards in the database."""
    if len(Card.select()) > 0:
        raise ValueError("There are cards in the database.")

    counter = 0
    for i in range(1, len(cnt_cards)):
        sum = 0
        for j in range(4, len(cnt_cards[i])):
            sum += cnt_cards[i][j]
        while sum > 0:
            create_card(
                id=counter,
                idtype=i,
                name=card_names[i][0],
                type=card_names[i][1],
            )
            sum -= 1
            counter += 1

    if counter != 104:
        raise ValueError("Wrong number of cards in the database.")


def create_card_asociation(deck: AvailableDeck, cnt_players: int):
    """Create asociation between cards and decks."""
    if len(Card.select()) == 0:
        create_all_cards()

    for i in range(1, len(cnt_cards)):
        sum = 0
        for j in range(4, cnt_players + 1):
            sum += cnt_cards[i][j]

        card_list = Card.select(idtype=i)
        for j in range(sum):
            add_available_deck_to_card(card_list[j].id, deck)
