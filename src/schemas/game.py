from typing import List
from typing import Optional

from pydantic import BaseModel
from schemas.player import PlayerOut




class GameStatus(BaseModel):
    alive_players: int
    the_thing_is_alive: bool
    current_turn: int
    turn_phase: str
    players: List[PlayerOut]
    lastPlayedCard: Optional[int]
