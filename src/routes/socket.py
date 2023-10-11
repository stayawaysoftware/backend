from core.connections import ConnectionManager
from core.connections import GAME_EVENT_TYPES
from core.connections import ROOM_EVENT_TYPES
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

connection_manager = ConnectionManager()
ws = APIRouter(tags=["websocket"])


@ws.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int):
    await connection_manager.connect(websocket, room_id, user_id)
    room_info = connection_manager.make_room_response(room_id, "info")
    await connection_manager.send_to(websocket, room_info)
    try:
        while True:
            try:
                data = await websocket.receive_json()
                if data["type"] == "message":
                    await connection_manager.broadcast(room_id, data)
                elif data["type"] in ROOM_EVENT_TYPES:
                    # TODO: Implement room events
                    pass
                elif data["type"] in GAME_EVENT_TYPES:
                    # TODO: Implement game events
                    pass
            except ValueError:
                # If the data is not a valid json close the connection
                await websocket.close()
                break

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room_id, user_id)
