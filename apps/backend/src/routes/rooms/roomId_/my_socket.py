import json

from typing import Dict

from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

from database.schemas import UserBase

from ...tokens import validate, fetchUser

class Connector:
    def __init__(self):
        self.connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        await websocket.accept()

        if room_id not in self.connections:
            self.connections[room_id] = {}

        self.connections[room_id][user_id] = websocket

    def disconnect(self, room_id: int, user_id: int):
        if room_id in self.connections and user_id in self.connections[room_id]:
            del self.connections[room_id][user_id]

            if not self.connections[room_id]:
                del self.connections[room_id]

    async def broadcast(self, text: str, room_id: int, user: UserBase):
        if not room_id in self.connections:
            return
        
        for _, connection in self.connections[room_id].items():
            await connection.send_json({
                "text": text,
                "author": json.dumps(user),
            })

manager = Connector()

def main(app: FastAPI):
    @app.websocket("/api/rooms/{room_id}")
    async def execute(websocket: WebSocket, room_id: int):
        token = websocket.query_params.get("authorization")
        token_valided = validate(token)

        if not token_valided or not token:
            return JSONResponse("False token", 403)

        _, user = fetchUser(token)

        await manager.connect(websocket, room_id, user.id)
        
        try:
            while True:
                data = await websocket.receive_json()
                await manager.broadcast(f"{data["text"]}", room_id, user)
        except:
            manager.disconnect(room_id, user.id)

    return execute