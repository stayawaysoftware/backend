from typing import Dict
from typing import List

from fastapi import WebSocket
from models.room import Room
from pony.orm import db_session

ROOM_EVENT_TYPES = ["leave", "start"]  # "join" is handled by the HTTP endpoint
GAME_EVENT_TYPES = ["play", "defend", "pass"]


class ConnectionManager:
    """Manage active connections to the websocket server"""

    def __init__(self):
        """Initialize the connection manager"""
        # Track active connections and the rooms they are in
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.user_rooms: Dict[int, int] = {}

    # ===================== CONNECTION METHODS =====================

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        # Check if the user is already in another room
        if user_id in self.user_rooms and self.user_rooms[user_id] != room_id:
            await websocket.close()

        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

        # Associate the user with the current room
        self.user_rooms[user_id] = room_id

    def disconnect(self, websocket: WebSocket, room_id: int, user_id: int):
        self.active_connections[room_id].remove(websocket)
        # Delete the user-room association
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]

    # ===================== MAKE RESPONSE METHODS =====================

    def make_room_response(self, room_id: int, type: str):
        with db_session:
            room = Room.get(id=room_id)
            users = list(room.users)
            users.sort(key=lambda x: x.id)
            usernames = [u.username for u in users]
            response = {
                "type": type,
                "room": {
                    "id": room_id,
                    "name": room.name,
                    "host": room.host_id,
                    "users": {
                        "min": room.min_users,
                        "max": room.max_users,
                        "names": usernames,
                    },
                },
            }
        return response

    def make_game_response(self, room_id: int, type: str):
        # TODO: Implement this method with game needed data
        pass

    def make_error(self, message: str):
        return {"type": "error", "error": message}

    # ===================== SEND METHODS =====================

    async def send_to(self, websocket: WebSocket, message: str):
        await websocket.send_json(message)

    async def broadcast(self, room_id: int, msg: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(msg)
