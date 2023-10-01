from fastapi import APIRouter
from fastapi import HTTPException
from models.game import Game
from pony.orm import db_session
from schemas.game import gameStatus
from schemas.game import Player

game = APIRouter(tags=["game"])


@game.get(
    "/game/{game_id}",
    response_model=gameStatus,
    response_description="Game actual status",
)
def get_game_status(game_id: int):
    with db_session:
        if not Game.exists(id=game_id):
            raise HTTPException(status_code=500, detail="Game does not exists")
        players = Game.get(id=game_id).players
        player_list = [Player.from_orm(p) for p in players]
        gameS = gameStatus(
            players=player_list,
            alive_players=len(player_list),
            the_thing_is_alive=True,
            turn_phase="Draw",
        )
    return gameS
