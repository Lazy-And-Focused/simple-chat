from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.schemas import AuthBase
from database.session import Database

from ..globals import codes
from ..tokens import validate, fetch

import hash
import time

def authenticateByPassword(req: Request):
    key = req.headers.get("key")
    email = req.headers.get("email")
    password = req.headers.get("password")

    if not email or not password:
        return JSONResponse("Not email or password", status_code=400)

    password = hash.hash(key or email, password)
    auth = Database(AuthBase).getByKey("email", email)

    if auth[0].password != password:
        return JSONResponse("Invalid password", status_code=403)
    
    return {
        "id": f"{auth[0].id}",
        "access_token": f"{auth[0].access_token}",
        "user_id": f"{auth[0].user_id}",
        "email": f"{auth[0].email}"
    }

def authenticate(req: Request):
    token = req.headers.get("authorization")
    token_valided = validate(token)
    
    if not token_valided or not token:
        return authenticateByPassword(req)
        
    auth = fetch(token)  
    
    return {
        "id": f"{auth.id}",
        "access_token": f"{auth.access_token}",
        "user_id": f"{auth.user_id}",
        "email": f"{auth.email}"
    }

def main(app: FastAPI):
    @app.get("/api/auth")
    def execute(req: Request):
        code = req.query_params.get("code")

        if not code:
            return authenticate(req)

        if not code in codes:
            return authenticate(req)

        email, expires_time = codes[code]

        if expires_time - int(time.time()) <= 0:
            return JSONResponse("Code expired", 403)

        auth = Database(AuthBase).getByKey("email", email)

        if len(auth) == 0:
            return JSONResponse("Bad code", 400)

        return {
            "id": f"{auth[0].id}",
            "access_token": f"{auth[0].access_token}",
            "user_id": f"{auth[0].user_id}",
            "email": f"{auth[0].email}"
        }
    
    return execute