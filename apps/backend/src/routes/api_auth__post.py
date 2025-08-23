from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.schemas import AuthBase, UserBase
from database.session import Database
from pydantic import BaseModel

from .globals import codes

import hash
import time

class UserDto(BaseModel):
  username: str
  name: Optional[str]
  avatar_url: Optional[str]
  
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

        if (len(Database(AuthBase).getByKey("email", email)) != 0):
            return JSONResponse("already created", 409)

        Database(UserBase).create(UserBase(
            username=user["username"],
            avatar_url=(user["avatar_url"] if "avatar_url" in user else ""),
            name=(user["name"] if "name" in user else "")
        )) # type: ignore
        databaseUser = Database(UserBase).getByKey("username", user["username"])[0]
        Database(AuthBase).create(AuthBase(
            user_id=databaseUser.id,
            email=email,
            password=password,
            access_token=hash.createHash(f"{email}{password}{databaseUser.username}{databaseUser.id}").hex()
        ))

        code = int(time.time())
        codes[str(code)] = (email, code + 5 * 60 * 1000) # 5 minutes

        return code
    
    return execute