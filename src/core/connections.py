from typing import Dict
from typing import List

from fastapi import WebSocket


class ConnectionManager:
    """Manage active connections to the websocket server"""

    def __init__(self):
        """Initialize the connection manager"""
        # Track active connections and the rooms they are in
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.user_rooms: Dict[int, int] = {}
        self.user_sockets: Dict[int, WebSocket] = {}

    # ===================== CONNECTION METHODS =====================

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        # Check if the user is already in a room
        #if user_id in self.user_rooms:
        #    await websocket.close()

        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

        # Associate the user with the current room
        self.user_rooms[user_id] = room_id

        # Associate the user with the current socket
        self.user_sockets[user_id] = websocket

    async def disconnect(
        self, websocket: WebSocket, room_id: int, user_id: int
    ):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
        # Delete the user-room association
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]

        # Delete the user-socket association
        if user_id in self.user_sockets:
            del self.user_sockets[user_id]

        if websocket:
            try:
                await websocket.close()
            except RuntimeError:
                pass

    async def disconnect_all(self, room_id: int):

        # Delete all user-room associations for the room
        users_to_remove = [
            user_id
            for user_id, room in self.user_rooms.items()
            if room == room_id
        ]

        for user_id in users_to_remove:
            del self.user_rooms[user_id]

        # Delete all user-socekt associations for the room
        for user_id in users_to_remove:
            del self.user_sockets[user_id]

        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.close()
            del self.active_connections[room_id]

    # ===================== SEND METHODS =====================

    async def send_to(self, websocket: WebSocket, message: str):
        await websocket.send_json(message)

    async def send_to_user_id(self, user_id: int, message: str):
        if user_id in self.user_sockets:
            await self.user_sockets[user_id].send_json(message)

    async def broadcast(self, room_id: int, msg: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(msg)
