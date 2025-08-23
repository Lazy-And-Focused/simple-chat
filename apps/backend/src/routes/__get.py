from fastapi import FastAPI

def main(app: FastAPI):
    @app.get("/")
    def execute(): 
        return "hello"
    
    return execute