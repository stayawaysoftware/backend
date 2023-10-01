from typing import List

from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str
    position: int
    is_alive: bool
    role: str


class GameStatus(BaseModel):
    alive_players: int
    the_thing_is_alive: bool
    actual_turn: int
    turn_phase: str
    players: List[Player]
