from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.schemas import AuthBase, UserBase
from database.session import Database

import time
import hash

from pydantic import BaseModel

class UserDto(BaseModel):
  username: str
  name: Optional[str]
  avatar_url: Optional[str]

app = FastAPI()
 
codes: dict[str, str] = {}

@app.get("/")
def read_root():
  return

@app.post("/api/auth")
async def auth(req: Request):
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
    password=password
  ))

  code = int(time.time())
  codes[str(code)] = email

  return code

@app.get("/api/auth")
def getAuth(req: Request):
  code = req.query_params.get("code")

  if not code:
    return JSONResponse("Forbidenn", 403)
  
  if not code in codes:
    return JSONResponse("Bad code", 400)

  email = codes[code]
  auth = Database(AuthBase).getByKey("email", email)

  if len(auth) == 0:
    return JSONResponse("Bad code", 400)

  return auth[0]