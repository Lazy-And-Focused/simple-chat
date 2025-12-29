from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.schemas import AuthBase, UserBase
from database.session import Database

from ..globals import codes
from ..tokens import generateToken

import hash
import time

FIVE_MINUTES = 5 * 60 * 1000

def main(app: FastAPI):
    @app.post("/api/auth")
    async def execute(req: Request):
        key = req.headers.get("key")
        email = req.headers.get("email")
        password = req.headers.get("password")

        user = await req.json()

        if not email or not password:
            return JSONResponse("Not email or password", status_code=400)

        if not "username" in user:
            return JSONResponse("Bad body", status_code=400)

        password = hash.hash(key or email, password)

        exists = len(Database(AuthBase).getByKey("email", email)) != 0
        if (exists):
            return JSONResponse("already created", 409)

        avatar_url = user["avatar_url"] if "avatar_url" in user else ""
        name = user["name"] if "name" in user else ""

        Database(UserBase).create(UserBase(
            username=user["username"],
            avatar_url=avatar_url,
            name=name
        ))

        databaseUser = Database(UserBase).getByKey("username", user["username"])[0]
        hashData, access_token = generateToken(databaseUser.id, email, password)

        Database(AuthBase).create(AuthBase(
            user_id=databaseUser.id,
            email=email,
            password=password,
            hash=hashData,
            access_token=access_token
        ))

        code = int(time.time())
        codes[str(code)] = (email, code + FIVE_MINUTES)

        return code
    
    return execute