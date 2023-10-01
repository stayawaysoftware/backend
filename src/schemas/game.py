from pydantic import BaseModel
from typing import List

class Player(BaseModel):
    id: int
    name: str
    position: int
    is_alive: bool
    role: str


class gameStatus(BaseModel):
    alive_players: int
    the_thing_is_alive: bool
    actual_turn: int
    turn_phase: str
    players: List[Player]