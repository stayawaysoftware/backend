import core.game_utility as gu
from fastapi import APIRouter
from fastapi import HTTPException
from core.effects import do_effect
from models.game import Game
from models.game import Player
from models.game import Card
from pony.orm import db_session
from pony.orm import commit
from schemas.game import GameStatus
from schemas.player import PlayerOut
from typing import Optional

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
        players = Game.get(id=game_id).players
        player_list = [PlayerOut.from_player(p) for p in players]
        game_status = GameStatus(
            players=player_list,
            alive_players=len(player_list),
            the_thing_is_alive=True,
            turn_phase="Draw",
            current_turn=Game.get(id=game_id).current_position,
        )
    return game_status

@game.put(
    "/game/{game_id}/play_card",
    response_model=GameStatus,
    response_description="Updated Status after play a card",
)
def play_card(game_id: int, card_idtype: int,current_player_id: int, target_player_id: Optional[int] = None):
    with db_session:
        current_game = Game.get(id=game_id)
        if not Game.exists(id=game_id):
            raise HTTPException(status_code=404, detail="Game not found")
        current_game.current_phase = "Play"
        commit()
        current_player = Player.get(id=current_player_id)
        effect = do_effect(id_game=game_id,id_card_type=card_idtype,target=target_player_id)
        gu.discard_card(id_game=game_id,id_card_type=card_idtype,player=current_player)
        if str(effect.get_action()) == "Kill":
            target_player = Player.get(id=target_player_id)
            target_player.alive = False
            commit()
        players = Game.get(id=game_id).players
        player_list = [PlayerOut.from_player(p) for p in players]
        game_status = GameStatus(
            players=player_list,
            alive_players=len(player_list),
            the_thing_is_alive=True,
            turn_phase="Draw",
            current_turn=Game.get(id=game_id).current_position,
        )
    return game_status

        

