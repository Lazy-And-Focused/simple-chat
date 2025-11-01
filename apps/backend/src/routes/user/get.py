from typing import cast

from fastapi import FastAPI, Request

from ...database.schemas.user import UserBase
from ...database.schemas.auth import AuthBase

from ..tokens import fetchUserByRequest

UserData = tuple[AuthBase, UserBase]

def main(app: FastAPI):
    @app.get("/api/user")
    def execute(request: Request):
        successed, data = fetchUserByRequest(request)

        if not successed:
            return data

        _, user = cast(UserData, data)

        return user
 
    return execute