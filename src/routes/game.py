from fastapi import APIRouter
from fastapi import HTTPException
from models.game import Game
from models.game import Player
from pony.orm import db_session
from pony.orm import session
from schemas.game import gameStatus

game = APIRouter(tags=["game"])

@game.get(
    "/game/{game_id}",
    response_model=gameStatus,
    response_description="Game actual status",
) 
def get_game_status(game_id: int):
    with db_session:
        pass