import core.room as rooms
from core.connections import ConnectionManager
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from pony.orm import db_session
from pydantic import ValidationError
from core.game import handle_play
from core.game import handle_defense
from schemas.socket  import GameMessage
from schemas.room import RoomEventValidator
from schemas.socket import ChatMessage
from schemas.socket import ErrorMessage
from schemas.socket import GameEventTypes
from schemas.socket import RoomEventTypes
from schemas.socket import RoomMessage

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
                        message = ChatMessage.create(
                            data["message"], user_id, room_id
                        )
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
                                    rooms.leave_room(
                                        validated_data.room_id,
                                        validated_data.user_id,
                                    )
                                    await connection_manager.disconnect(
                                        websocket, room_id, user_id
                                    )
                                    await connection_manager.broadcast(
                                        validated_data.room_id,
                                        RoomMessage.create(
                                            data["type"],
                                            validated_data.room_id,
                                        ),
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
                        try:
                            match data["type"]:
                                case "play":
                                    response = handle_play(
                                        data["played_card"],
                                        data["card_target"],
                                    )
                                    await connection_manager.broadcast(room_id, response)
                                case "defense":
                                    await handle_defense(
                                        room_id,
                                        data["card_type_id"],
                                        user_id,
                                        data["last_card_played_id"],
                                        data["attacker_id"],
                                    )
                                    await connection_manager.broadcast(
                                        room_id,
                                        GameMessage.create(
                                            data["type"], room_id
                                        ),
                                    )
                                case _:
                                    await connection_manager.send_to(
                                        websocket,
                                        ErrorMessage.create(
                                            "DEBUGGING: Invalid game event"
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

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room_id, user_id)
