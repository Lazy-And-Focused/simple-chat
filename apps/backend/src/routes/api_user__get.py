from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .tokens import validate, fetchUser

def main(app: FastAPI, _):
    @app.get("/api/user")
    def execute(request: Request):
        token = request.headers.get("authorization")
        tokenValided = validate(token)
        
        if not tokenValided or not token:
            return JSONResponse("False token", 403)

        _, user = fetchUser(token)  

        return user
    
    return execute