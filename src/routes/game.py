from typing import Optional

from core.game import calculate_next_turn
from core.game import play_card
from core.game_utility import draw_card_from_deck
from core.room import delete_room
from fastapi import APIRouter
from fastapi import HTTPException
from models.game import Game
from models.game import Player
from models.room import Room
from pony.orm import commit
from pony.orm import db_session
from schemas.game import GameStatus
from schemas.player import PlayerOut
from fastapi import status
from fastapi import Response


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
        the_thing_player = Player.get(role="The Thing")
        the_thing_player_status = the_thing_player.alive
        game_status = GameStatus(
            players=player_list,
            alive_players=len(player_list),
            the_thing_is_alive=the_thing_player_status,
            turn_phase=Game.get(id=game_id).current_phase,
            current_turn=Game.get(id=game_id).current_position,
            lastPlayedCard=None,
        )
    return game_status


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
        play_card(
            game_id=game_id,
            card_idtype=card_idtype,
            current_player_id=current_player_id,
            target_player_id=target_player_id,
        )
        players = Game.get(id=game_id).players
        player_list = [PlayerOut.from_player(p) for p in players]
        calculate_next_turn(game_id=game_id)
        next_player = Player.get(round_position=current_game.current_position)
        draw_card_from_deck(id_game=game_id, player=next_player)
        current_game.current_phase = "Draw"
        commit()
        the_thing_player = Player.get(role="The Thing")
        the_thing_player_status = the_thing_player.alive

        game_status = GameStatus(
            players=player_list,
            alive_players=len(player_list),
            the_thing_is_alive=the_thing_player_status,
            turn_phase=Game.get(id=game_id).current_phase,
            current_turn=Game.get(id=game_id).current_position,
            lastPlayedCard=card_idtype,
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
def delete_game(game_id: int):
    with db_session:
        game = Game.get(id=game_id)
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        if game.status != "Finished":
            raise HTTPException(status_code=400, detail="Game has not finished")
        players = Game.get(id=game_id).players
        if players is None:
            raise HTTPException(status_code=404, detail="Players not found")
        for p in players:
            p.delete()
        game.delete()
        commit()
        room = Room.get(id=game.id)
        delete_room(room.id, room.host_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)