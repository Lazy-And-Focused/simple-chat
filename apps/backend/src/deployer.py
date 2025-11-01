from typing import Any, Callable
from fastapi import FastAPI

import routes.auth.get as getAuth
import routes.auth.post as postAuth
import routes.auth.put as putAuth

import routes.rooms.roomId_.my_socket as my_socketRoomsRoomId_

import routes.user.get as getUser

routes: list[Callable[[FastAPI], Any]] = [
    getAuth.main,
    postAuth.main,
    putAuth.main,
    my_socketRoomsRoomId_.main,
    getUser.main,
]

def register(app: FastAPI):
    for route in routes:
        route(app)

if __name__ == "__main__":
    for route in routes:
        print(route)
