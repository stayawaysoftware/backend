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
from core.deck import *  # noqa : F401
from core.card import *  # noqa : F401
from core.game_utility import *  # noqa : F401
from core.effects import *  # noqa : F401
from core.game_action import *  # noqa : F401
from core.game_action import *  # noqa : F401
from core.effects import *  # noqa : F401
from core.card import *  # noqa : F401
from core.deck import *  # noqa : F401
from models import db  # noqa : F401
from models.room import Room  # noqa : F401
from models.room import User  # noqa : F401
from models.game import Game  # noqa : F401
from models.game import Player  # noqa : F401
from pony.orm import db_session, commit  # noqa : F401


# Generate the database mapping
db.bind(provider="sqlite", filename=":memory:", create_db=True)
db.generate_mapping(create_tables=True)
