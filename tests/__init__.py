import os
import sys

# Add src to path
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.append(src_dir)


from core.user import *  # noqa : F401
from core.room import *  # noqa : F401
from core.game import *  # noqa : F401
from core.player import *  # noqa : F401
from core.game_logic.deck import *  # noqa : F401
from core.game_logic.card import *  # noqa : F401
from core.game_logic.game_utility import *  # noqa : F401
from core.game_logic.game_effects import *  # noqa : F401
from core.game_logic.game_action import *  # noqa : F401
from core.game_logic.card_creation import *  # noqa : F401
from core.game_logic.effects.analysis_effect import *  # noqa : F401
from core.game_logic.effects.change_of_position_effect import *  # noqa : F401
from core.game_logic.effects.effect_handler import *  # noqa : F401
from core.game_logic.effects.exchange_effect import *  # noqa : F401
from core.game_logic.effects.flamethrower_effect import *  # noqa : F401
from core.game_logic.effects.nothing_effect import *  # noqa : F401
from core.game_logic.effects.suspicion_effect import *  # noqa : F401
from core.game_logic.effects.watch_your_back_effect import *  # noqa : F401
from core.game_logic.effects.whisky_effect import *  # noqa : F401
from models import db  # noqa : F401
from models.room import Room  # noqa : F401
from models.room import User  # noqa : F401
from models.game import Game  # noqa : F401
from models.game import Player  # noqa : F401
from models.game import Deck  # noqa : F401
from models.game import Card  # noqa : F401
from models.game import AvailableDeck  # noqa : F401
from models.game import DisposableDeck  # noqa : F401
from schemas.validators import SocketValidators  # noqa : F401
from schemas.validators import EndpointValidators  # noqa : F401
from pony.orm import db_session  # noqa : F401
from pony.orm import commit  # noqa : F401


# Generate the database mapping
db.bind(provider="sqlite", filename=":memory:", create_db=True)
db.generate_mapping(create_tables=True)

# Clean DB


@db_session
def clean_db():
    """Clean DB."""
    for x in Card.select():
        x.delete()
    for x in Deck.select():
        x.delete()
    for x in AvailableDeck.select():
        x.delete()
    for x in DisposableDeck.select():
        x.delete()
    for x in Game.select():
        x.delete()
    for x in Player.select():
        x.delete()
    for x in User.select():
        x.delete()
    for x in Room.select():
        x.delete()
    commit()
