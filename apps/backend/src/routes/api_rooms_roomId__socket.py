from typing import Dict

from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

from .tokens import validate, fetchUser
from database.schemas import UserBase

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    def disconnect(self, room_id: int, user_id: int):
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: str, room_id: int, user: UserBase):
        if room_id in self.active_connections:
            for _, connection in self.active_connections[room_id].items():
                message_with_class: Dict[str, str|int] = {
                    "text": message,
                    "author_id": user.id,
                    "author": user.username,
                }
                await connection.send_json(message_with_class)

manager = ConnectionManager()

def main(app: FastAPI, _):
    @app.websocket("/api/rooms/{room_id}")
    async def execute(websocket: WebSocket, room_id: int):
        token = websocket.query_params.get("authorization")
        tokenValided = validate(token)

        if not tokenValided or not token:
            return JSONResponse("False token", 403)

        _, user = fetchUser(token)

        await manager.connect(websocket, room_id, user.id)
        
        try:
            await manager.broadcast(f"Hello, i'm join to chat", room_id, user)

            while True:
                data = await websocket.receive_json()
                await manager.broadcast(f"{data["text"]}", room_id, user)
        except:
            manager.disconnect(room_id, user.id)
            await manager.broadcast(f"Goodbye, i'm left from chat", room_id, user)

    return execute