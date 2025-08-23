from typing import Any, Callable, Final
from fastapi import FastAPI

import re
import os
import importlib

ROUTES_DIR: Final[str] = "routes"

ROUTES = list(filter(lambda x: x.endswith(".py"), os.listdir(ROUTES_DIR)))
ROUTE_REX_EX = r"(?:.*_?)*__.*"

def main() -> dict[str, Callable[[Any], Any]]:
    modules: dict[str, Callable[[Any], Any]] = {}

    for route in ROUTES:
        data, _ = route.split(".")
        
        if re.match(ROUTE_REX_EX, data) == None: continue

        path, method = data.split("__")

        module: Any = importlib.import_module(f"{ROUTES_DIR}.{path}__{method}")
        modules[f"{path.replace("_", "/")}.{method}"] = module.main

    return modules

def register(app: FastAPI):
    routes = main()

    for route in routes:
        routes[route](app)

if __name__ == "__main__":
    routes = main()

    for route in routes:
        print(route)
        print(routes[route])