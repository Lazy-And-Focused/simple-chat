from typing import Dict

from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

from .tokens import validate, fetch

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

    async def broadcast(self, message: str, room_id: int, sender_id: int):
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items():
                message_with_class: Dict[str, str|bool] = {
                    "text": message,
                    "is_self": user_id == sender_id
                }
                await connection.send_json(message_with_class)

manager = ConnectionManager()

def main(app: FastAPI, _):
    @app.websocket("/api/rooms/{room_id}")
    async def execute(websocket: WebSocket, room_id: int):
        token = websocket.headers.get("Authorization")
        tokenValided = validate(token)

        if not tokenValided or not token:
            return JSONResponse("False token", 403)

        auth = fetch(token)

        await manager.connect(websocket, room_id, auth.id)
        
        return

        try:
            while True:
                data = await websocket.receive_text()
                await manager.send_personal_message(f"You wrote: {data}", websocket)
                await manager.broadcast(f"Client #{websocket.client_state.name} says: {data}")
        except:
            manager.disconnect(websocket)
            await manager.broadcast(f"Client #{websocket.client_state.name} left the chat")

    return execute