from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.schemas import UserBase
from database.session import Database

from .tokens import validate, fetch

def main(app: FastAPI, _):
    @app.get("/api/user")
    def execute(request: Request):
        token = request.headers.get("Authorization")
        tokenValided = validate(token)
        
        if not tokenValided or not token:
            return JSONResponse("False token", 403)

        auth = fetch(token)  
        user = Database(UserBase).getById(auth.user_id)

        return user
    
    return execute