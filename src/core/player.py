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
def get_alive_neighbors(id_game: int, id_player: int):
    """Return the list of alive neighbors of a player."""
    if not Game.exists(id=id_game):
        raise ValueError(f"Game with id {id_game} doesn't exist")
    if not Player.exists(id=id_player):
        raise ValueError(f"Player with id {id_player} doesn't exist")

    player = Player[id_player]
    current_position = player.round_position

    player_list = list(Game[id_game].players)
    player_list.sort(key=lambda x: x.round_position)

    cnt_players = len(player_list)

    neighbor_list = []

    for direction in [-1, 1]:
        neighbor_position = current_position
        break_condition = False

        while (
            neighbor_position is current_position
            or not player_list[neighbor_position - 1].alive
        ):
            neighbor_position = (
                (neighbor_position - 1) + direction + cnt_players
            ) % cnt_players + 1

            if neighbor_position == current_position:
                break_condition = True
                break

        if not break_condition:
            neighbor_list.append(player_list[neighbor_position - 1].id)

    return neighbor_list
