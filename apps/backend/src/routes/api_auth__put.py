from fastapi import FastAPI

def main(app: FastAPI, _):
    @app.put("/api/auth")
    def execute(): 
        return "hello"
    
    return execute