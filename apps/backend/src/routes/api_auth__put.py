from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.schemas import AuthBase
from database.session import Database

from .tokens import validate, fetch, generateToken

import hash

def main(app: FastAPI, _):
    @app.put("/api/auth")
    async def execute(req: Request):
        token = req.headers.get("Authorization")
        tokenValided = validate(token)
        
        if not tokenValided or not token:
            return JSONResponse("False token", 403)

        auth = fetch(token)
        key = req.headers.get("key")
        password = req.headers.get("password")
        email = req.headers.get("email") or auth.email

        newToken: str

        if password:
            password = hash.hash(key or email, password)
            hashData, access_token = generateToken(auth.user_id, email, password)
            newToken = access_token
            Database(AuthBase).update(AuthBase(
                *auth,
                email=email,
                hash=hashData,
                password=password,
                access_token=access_token
            ))
        else:
            hashData, access_token = generateToken(auth.user_id, email, auth.password)
            newToken = access_token
            Database(AuthBase).update(AuthBase(
                *auth,
                email=email,
                hash=hashData,
                access_token=access_token
            ))

        return newToken
    
    return execute