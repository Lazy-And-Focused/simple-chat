from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

import deployer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "PATCH"],
    allow_headers=["key", "password", "email", "authorization"]
)

deployer.register(app)