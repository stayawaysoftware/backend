from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from models.game import Game
from schemas.player import PlayerOut


class GameStatus(BaseModel):
    alive_players: int
    the_thing_is_alive: bool
    current_turn: int
    turn_phase: str
    players: List[PlayerOut]
    lastPlayedCard: Optional[int]

class PlayersInfo(BaseModel):
    model_config = ConfigDict(title="Users", from_attributes=True)

    min: int = Field(gt=3, lt=13)
    max: int = Field(gt=3, lt=13)
    names: list[str]

    @classmethod
    def get_players_info(cls, game: Game):
        players = list(game.users)
        #remove player.hand from the response
        for player in players:
            del player.hand
        players.sort(key=lambda player: player.id)
        return {
            "players" : players
        }


class GameInfo(BaseModel):
    model_config = ConfigDict(title="Room", from_attributes=True)

    players: PlayersInfo
    turn_phase: str
    current_turn: int
    turn_order : bool 


    @classmethod
    def from_db(cls, game: Game):
        return {
            "players": PlayersInfo.get_players_info(game),
            "turn_phase": game.current_phase,
            "current_turn": game.current_position,
            "turn_order": game.round_left_direction
        }
