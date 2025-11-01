from typing import cast

from fastapi import FastAPI, Request

from database.schemas import AuthBase
from database.session import Database

from ..tokens import fetchByRequest, generateToken

import hash

def updateAuth(key: str|None, password: str|None, email: str, auth: AuthBase):
    hashedPassword: str|None = None

    if password != None and key != None:
        hashedPassword = hash.hash(key, password)
    
    hashData, access_token = generateToken(auth.user_id, email, hashedPassword or auth.password)
    Database(AuthBase).update(AuthBase(
        *auth,
        email=email,
        hash=hashData,
        password=(hashedPassword or auth.password),
        access_token=access_token
    )) 

    return access_token

def main(app: FastAPI):
    @app.put("/api/auth")
    async def execute(req: Request):
        successed, data = fetchByRequest(req)

        if not successed:
            return data
        
        auth = cast(AuthBase, data)

        key = req.headers.get("key")
        password = req.headers.get("password")
        email = req.headers.get("email") or auth.email

        if password:
            newToken = updateAuth(key or email, password, email, auth)
        else:
            newToken = updateAuth(email=email, auth=auth, password=None, key=None)

        return newToken
    
    return execute