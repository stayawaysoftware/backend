import core.room as rooms
from core.connections import ConnectionManager
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from pony.orm import db_session
from pydantic import ValidationError
from core.game import handle_game_event
from schemas.socket  import GameMessage
from schemas.room import StartGameValidator
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
                                validated_data = StartGameValidator.validate(
                                    room_id, user_id
                                )
                                with db_session:
                                    rooms.start_game(
                                        validated_data.room_id,
                                        validated_data.user_id,
                                    )

                                await connection_manager.broadcast(
                                    room_id,
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
                            pass

                        case _:
                            await connection_manager.send_to(
                                websocket,
                                ErrorMessage.create(
                                    "DEBUGGING: Invalid room event"
                                ),
                            )
                elif GameEventTypes.has_type(data["type"]):
                    while True:
                        game_info = GameMessage.create("info", room_id)
                        await connection_manager.send_to(websocket, game_info)
                        try:
                            handle_game_event(
                            data=data, room_id=room_id, user_id=user_id
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
