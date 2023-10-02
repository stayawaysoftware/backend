from fastapi import APIRouter
from fastapi import HTTPException
from models.game import Game
from pony.orm import db_session
from schemas.game import GameStatus
from schemas.player import PlayerOut

game = APIRouter(tags=["game"])


@game.get(
    "/game/{game_id}",
    response_model=GameStatus,
    response_description="Game actual status",
)
def get_game_status(game_id: int):
    with db_session:
        if not Game.exists(id=game_id):
            raise HTTPException(status_code=500, detail="Game does not exists")
        players = Game.get(id=game_id).players
        player_list = [PlayerOut.from_player(p) for p in players]
        game_status = GameStatus(
            players=player_list,
            alive_players=len(player_list),
            the_thing_is_alive=True,
            turn_phase="Draw",
            current_turn=Game.get(id=game_id).current_position
        )
    return game_status
