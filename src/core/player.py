from pony.orm import db_session, commit
from models.game import Deck
from models.game import Game
from models.game import Player
from models.room import Room
import core.game_utility as gu


@db_session
def create_player(room_id: int, game: Game, user_id: int, p_round_position: int):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (cP)")

    #get a user in a room by id
    user = None
    for u in room.users:
        if u.id == user_id:
            user = u
            break
    if user is None:
        raise ValueError("User does not exist")
    player = Player(
        name=user.username, id=user.id, round_position=p_round_position, game=game
    )
    commit()
    return player

@db_session
def dealing_cards(room_id: int, player: Player, index: int):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (dC)")
    if index == 1:
        gu.draw_card_from_deck(room_id, player)
    for i in range(4):
        gu.draw_card_from_deck(room_id, player)