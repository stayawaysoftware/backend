from core.connections import ConnectionManager
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from pydantic import ValidationError
from schemas.socket import ChatMessageIn
from schemas.socket import ChatMessageOut
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
                            connection_manager.make_error("Invalid message"),
                        )
                        continue
                elif RoomEventTypes.has_type(data["type"]):
                    # TODO: Implement this
                    pass
                elif GameEventTypes.has_type(data["type"]):
                    # TODO: Implement this
                    pass
            except ValueError:
                # If the data is not a valid json close the connection
                await websocket.close()
                break

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room_id, user_id)

    except AttributeError:
        # If the data is not a valid json close the connection
        await websocket.close()
