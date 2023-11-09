import core.game_logic.game_utility as gu
from models.game import Game
from models.game import Player
from models.room import Room
from pony.orm import commit
from pony.orm import db_session


@db_session
def create_player(
    room_id: int, game: Game, user_id: int, p_round_position: int
):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (cP)")

    # get a user in a room by id
    user = None
    for u in room.users:
        if u.id == user_id:
            user = u
            break
    if user is None:
        raise ValueError("User does not exist")
    player = Player(
        name=user.username,
        id=user.id,
        round_position=p_round_position,
        game=game,
    )
    commit()
    return player


@db_session
def dealing_cards(room_id: int, player: Player, index: int):
    room = Room.get(id=room_id)
    if room.in_game:
        raise PermissionError("Game is in progress (dC)")
    if index == 1:
        available_deck = gu.get_deck(room_id).available_deck
        cards = list(available_deck.cards)
        # Get card with idtype 1
        i = 0
        card = cards[i]
        while card.idtype != 1:
            i += 1
            card = cards[i]
        gu.unrelate_card_with_available_deck(card.id, room_id)
        gu.relate_card_with_player(card.id, player.id)
    for i in range(4):
        gu.draw(room_id, player.id)
