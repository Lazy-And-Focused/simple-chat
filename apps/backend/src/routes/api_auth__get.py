from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.schemas import AuthBase
from database.session import Database

from .globals import codes
from .tokens import validate, fetchUser

import time

def main(app: FastAPI, _):
    @app.get("/api/auth")
    def execute(req: Request):
        code = req.query_params.get("code")

        if not code:
            token = req.headers.get("authorization")
            tokenValided = validate(token)
            
            if not tokenValided or not token:
                return JSONResponse("False token", 403)
        
            _, user = fetchUser(token)  
            
            return user
        
        if not code in codes:
            return JSONResponse("Bad code", 400)

        email, expiresTime = codes[code]

        if expiresTime - int(time.time()) <= 0:
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