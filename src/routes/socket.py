from time import sleep

import core.room as rooms
from core.connections import ConnectionManager
from core.game import get_card_idtype
from core.game import handle_cannot_exchange
from core.game import handle_defense
from core.game import handle_discard
from core.game import handle_exchange
from core.game import handle_exchange_defense
from core.game import handle_not_target
from core.game import handle_play
from core.game import try_defense
from core.room import delete_game
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from models.game import Player
from pony.orm import db_session
from pydantic import ValidationError
from schemas.room import RoomEventValidator
from schemas.socket import ChatMessage
from schemas.socket import ErrorMessage
from schemas.socket import GameEventTypes
from schemas.socket import GameMessage
from schemas.socket import RoomEventTypes
from schemas.socket import RoomMessage

PRIVATE_CARDTYPES = [4, 6, 14, 27, 31]

connection_manager = ConnectionManager()
ws = APIRouter(tags=["websocket"])


@ws.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int):
    # On new or join connect and get info
    await connection_manager.connect(websocket, room_id, user_id)
    try:
        room_info = RoomMessage.create("info", room_id)
        await connection_manager.send_to(websocket, room_info)
        while True:
            try:
                data = await websocket.receive_json()
                if data["type"] == "message":
                    try:
                        ChatMessage.validate(user_id, room_id)
                        message = ChatMessage.create(data["message"], user_id)
                        await connection_manager.broadcast(room_id, message)
                    except ValidationError as error:
                        await connection_manager.send_to(
                            websocket,
                            ErrorMessage.create(str(error)),
                        )
                    except KeyError:
                        await connection_manager.send_to(
                            websocket,
                            ErrorMessage.create("DEBUGGING: Invalid message"),
                        )
                elif RoomEventTypes.has_type(data["type"]):
                    match data["type"]:
                        case "start":
                            try:
                                validated_data = RoomEventValidator.validate(
                                    data["type"], room_id, user_id
                                )

                                with db_session:
                                    rooms.start_game(
                                        validated_data.room_id,
                                        validated_data.user_id,
                                    )

                                await connection_manager.broadcast(
                                    validated_data.room_id,
                                    RoomMessage.create(
                                        data["type"], validated_data.room_id
                                    ),
                                )
                                sleep(1)
                                await connection_manager.broadcast(
                                    room_id,
                                    GameMessage.create("game_info", room_id),
                                )
                            except ValidationError as error:
                                await connection_manager.send_to(
                                    websocket,
                                    ErrorMessage.create(str(error)),
                                )
                        case "leave":
                            try:
                                validated_data = RoomEventValidator.validate(
                                    data["type"], room_id, user_id
                                )
                                with db_session:
                                    if rooms.leave_room(
                                        validated_data.room_id,
                                        validated_data.user_id,
                                    ):
                                        await connection_manager.disconnect(
                                            websocket,
                                            validated_data.room_id,
                                            validated_data.user_id,
                                        )
                                        await connection_manager.broadcast(
                                            validated_data.room_id,
                                            RoomMessage.create(
                                                data["type"],
                                                validated_data.room_id,
                                            ),
                                        )
                                    else:
                                        await connection_manager.disconnect_all(
                                            validated_data.room_id
                                        )

                            except ValidationError as error:
                                await connection_manager.send_to(
                                    websocket,
                                    ErrorMessage.create(str(error)),
                                )
                        case _:
                            await connection_manager.send_to(
                                websocket,
                                ErrorMessage.create(
                                    "DEBUGGING: Invalid room event"
                                ),
                            )
                elif GameEventTypes.has_type(data["type"]):
                    player = Player.get(id=user_id)
                    try:
                        match data["type"]:
                            case "play":
                                response = handle_play(
                                    room_id,
                                    data["played_card"],
                                    data["card_target"],
                                )
                                await connection_manager.broadcast(
                                    room_id, response
                                )

                                if data["card_target"] == user_id:
                                    response, effect = handle_not_target(
                                        room_id,
                                        data["played_card"],
                                        user_id,
                                    )

                                    if effect is not None:
                                        await connection_manager.broadcast(
                                            room_id, effect
                                        )

                                    await connection_manager.broadcast(
                                        room_id,
                                        GameMessage.create(
                                            "game_info", room_id
                                        ),
                                    )
                                else:
                                    defense_response = try_defense(
                                        room_id,
                                        data["played_card"],
                                        data["card_target"],
                                    )
                                    await connection_manager.broadcast(
                                        room_id, defense_response
                                    )

                            case "defense":
                                response, effect = handle_defense(
                                    game_id=room_id,
                                    card_type_id=data["played_defense"],
                                    attacker_id=data["target_player"],
                                    last_card_played_id=data[
                                        "last_played_card"
                                    ],
                                    defense_player_id=user_id,
                                )

                                await connection_manager.broadcast(
                                    room_id, response
                                )
                                private_attack = (
                                    get_card_idtype(data["last_played_card"])
                                    in PRIVATE_CARDTYPES
                                )
                                private_defense = (
                                    get_card_idtype(data["played_defense"])
                                    in PRIVATE_CARDTYPES
                                )
                                no_defense = data["played_defense"] == 0
                                if effect is not None:
                                    if private_attack and no_defense:
                                        await connection_manager.send_to_user_id(
                                            data["target_player"], effect
                                        )
                                    elif private_defense:
                                        await connection_manager.send_to_user_id(
                                            user_id, effect
                                        )
                                    else:
                                        await connection_manager.broadcast(
                                            room_id, effect
                                        )

                                await connection_manager.broadcast(
                                    room_id,
                                    GameMessage.create("game_info", room_id),
                                )

                            case "exchange":
                                exchange_res = handle_exchange(
                                    user_id,
                                    data["chosen_card"],
                                    data["target_player"],
                                )

                                await connection_manager.broadcast(
                                    room_id, exchange_res
                                )

                            case "cannot_exchange":
                                (
                                    draw_response,
                                    next_player_id,
                                ) = handle_cannot_exchange(room_id)

                                await connection_manager.send_to_user_id(
                                    next_player_id, draw_response
                                )

                                await connection_manager.broadcast(
                                    room_id,
                                    GameMessage.create("game_info", room_id),
                                )

                            case "exchange_defense":
                                (
                                    draw_response,
                                    next_player_id,
                                    effect,
                                ) = handle_exchange_defense(
                                    game_id=room_id,
                                    current_player_id=user_id,
                                    exchange_requester=data[
                                        "exchange_requester_id"
                                    ],
                                    last_chosen_card=data["last_chose"],
                                    chosen_card=data["chosen_card"],
                                    is_defense=data["is_defense"],
                                )

                                private_defense = (
                                    get_card_idtype(data["chosen_card"])
                                    in PRIVATE_CARDTYPES
                                )
                                if effect is not None:
                                    if private_defense and data["is_defense"]:
                                        await connection_manager.send_to_user_id(
                                            user_id, effect
                                        )
                                    else:
                                        await connection_manager.broadcast(
                                            room_id, effect
                                        )

                                await connection_manager.send_to_user_id(
                                    next_player_id, draw_response
                                )

                                res = {"type": "exchange_end"}
                                await connection_manager.broadcast(
                                    room_id, res
                                )

                                await connection_manager.broadcast(
                                    room_id,
                                    GameMessage.create("game_info", room_id),
                                )

                            case "discard":
                                handle_discard(
                                    room_id, data["played_card"], user_id
                                )

                                res = {
                                    "type": "discard",
                                    "played_card": data["played_card"],
                                }

                                await connection_manager.broadcast(
                                    room_id,
                                    res,
                                )

                                await connection_manager.broadcast(
                                    room_id,
                                    GameMessage.create("game_info", room_id),
                                )

                            case "finished":
                                delete_game(room_id)

                            case "game_status":
                                await connection_manager.broadcast(
                                    room_id,
                                    GameMessage.create("game_info", room_id),
                                )

                            case _:
                                await connection_manager.send_to(
                                    websocket,
                                    ErrorMessage.create(
                                        "DEBUGGING: Invalid game event"
                                    ),
                                )
                        if player.quarantine > 0:
                            card_dict = {
                                "play": data.get("played_card", None),
                                "discard": data.get("played_card", None),
                                "defense": data.get("played_defense", None),
                                "exchange": data.get("chosen_card", None),
                                "exchange_defense": data.get(
                                    "chosen_card", None
                                ),
                                "cannot_exchange": None,
                            }
                            if card_dict[data["type"]] != 0:
                                await connection_manager.broadcast(
                                    room_id,
                                    GameMessage.create(
                                        "quarantine",
                                        room_id,
                                        user_id,
                                        card_dict[data["type"]],
                                    ),
                                )
                    except ValidationError as error:
                        await connection_manager.send_to(
                            websocket,
                            ErrorMessage.create(str(error)),
                        )
            except ValueError:
                # If the data is not a valid json
                # For now send an error message
                await connection_manager.send_to(
                    websocket, ErrorMessage.create("DEBUGGING: Invalid format")
                )
            except RuntimeError:
                break

    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket, room_id, user_id)
