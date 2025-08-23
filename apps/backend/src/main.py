from fastapi import FastAPI 

import deployer

app = FastAPI()

deployer.register(app)