from typing import Callable, Any
from fastapi import FastAPI

def main(app: FastAPI, routes: dict[str, Callable[[Any, Any], Any]]):
    data: list[str] = []
    for route in routes:
        path, method = route.split(".")
        data.append(f"{method.upper()} '{path}'")

    @app.get("/")
    def execute():
        return data
    
    return execute