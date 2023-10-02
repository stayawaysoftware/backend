from typing import List
from schemas.player import PlayerOut
from pydantic import BaseModel



class GameStatus(BaseModel):
    alive_players: int
    the_thing_is_alive: bool
    current_turn: int
    turn_phase: str
    players: List[PlayerOut]
