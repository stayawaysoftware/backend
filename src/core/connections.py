from typing import Dict
from typing import List

from fastapi import WebSocket
from models.room import Room
from pony.orm import db_session


class ConnectionManager:
    """Manage active connections to the websocket server"""

    def __init__(self):
        self.active_connections: Dict[
            int, List[WebSocket]
        ] = {}  # Track active connections

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int, user_id: int):
        self.active_connections[room_id].remove(websocket)

    async def send_to(self, websocket: WebSocket, message: str):
        await websocket.send_json(message)


class RoomConnectionManager(ConnectionManager):
    """Room connection manager for the websocket server"""

    def __init__(self):
        super().__init__()
        self.user_rooms: Dict[int, int] = {}  # Track user-room associations

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        # Check if the user is already in another room
        if user_id in self.user_rooms and self.user_rooms[user_id] != room_id:
            await websocket.close()

        await super().connect(websocket, room_id, user_id)

        # Associate the user with the current room
        self.user_rooms[user_id] = room_id

    def create_response(self, room_id: int, event: str):
        with db_session:
            room = Room.get(id=room_id)
            users = list(room.users)
            users.sort(key=lambda x: x.id)
            usernames = [u.username for u in users]
            response = {
                "event": event,
                "room": {
                    "id": room_id,
                    "name": room.name,
                    "host": room.host_id,
                    "users": usernames,
                },
            }
        return response

    async def room_broadcast(self, room_id: int, event: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(
                    self.create_response(room_id, event)
                )

    def disconnect(self, websocket: WebSocket, room_id: int, user_id: int):
        super().disconnect(websocket, room_id, user_id)

        # Delete the user-room association
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]
