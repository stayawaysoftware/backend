import core.room as rooms
from core.connections import ConnectionManager
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from pony.orm import db_session
from pydantic import ValidationError
from schemas.room import StartGameIn
from schemas.socket import ChatMessageIn
from schemas.socket import ChatMessageOut
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
                        ChatMessageIn.model_validate(data)
                        message = ChatMessageOut.create(
                            data["message"], user_id
                        )
                        await connection_manager.broadcast(room_id, message)
                    except ValidationError:
                        await connection_manager.send_to(
                            websocket,
                            ErrorMessage.create("DEBUGGING: Invalid message"),
                        )
                        continue
                elif RoomEventTypes.has_type(data["type"]):
                    match data["type"]:
                        case "start":
                            try:
                                data = StartGameIn.create(
                                    data["type"], room_id, user_id
                                )
                                await connection_manager.broadcast(
                                    room_id,
                                    RoomMessage.create(data.type, room_id),
                                )
                                with db_session:
                                    rooms.start_game(room_id, user_id)
                            except ValidationError as error:
                                await connection_manager.send_to(
                                    websocket,
                                    ErrorMessage.create(
                                        error.errors()[0]["msg"]
                                    ),
                                )
                        case _:
                            await connection_manager.send_to(
                                websocket,
                                ErrorMessage.create(
                                    "DEBUGGING: Invalid room event"
                                ),
                            )
                elif GameEventTypes.has_type(data["type"]):
                    pass

                else:
                    await connection_manager.send_to(
                        websocket,
                        ErrorMessage.create("DEBUGGING: Invalid event"),
                    )

            except ValueError:
                # If the data is not a valid json
                # For now send an error message
                await connection_manager.send_to(
                    websocket, ErrorMessage.create("DEBUGGING: Invalid format")
                )

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room_id, user_id)
