from typing import Optional

from core.game import delete_game
from core.game import init_game_status
from core.game import turn_game_status
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from models.game import Game
from pony.orm import db_session
from schemas.game import GameStatus


game = APIRouter(tags=["game"])


@game.get(
    "/game/{game_id}",
    response_model=GameStatus,
    response_description="Game actual status",
)
def get_game_status(game_id: int):
    with db_session:
        if not Game.exists(id=game_id):
            raise HTTPException(status_code=404, detail="Game not found")
    return init_game_status(game_id)


@game.put(
    "/game/{game_id}/play_turn",
    response_model=GameStatus,
    response_description="Updated Status after play a card",
)
def play_turn(
    game_id: int,
    card_idtype: int,
    current_player_id: int,
    target_player_id: Optional[int] = None,
):
    with db_session:
        current_game = Game.get(id=game_id)
        if not Game.exists(id=game_id):
            raise HTTPException(status_code=404, detail="Game not found")
        game_status = turn_game_status(
            current_game, card_idtype, current_player_id, target_player_id
        )

    return game_status


@game.delete(
    "/game/{game_id}/end_game",
    response_description="Deletes the match",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Game not found"},
        400: {"description": "Game has not finished"},
    },
)
def end_game(game_id: int):
    with db_session:
        game = Game.get(id=game_id)
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        if game.status != "Finished":
            raise HTTPException(
                status_code=400, detail="Game has not finished"
            )
        delete_game(game_id)
