from fastapi import FastAPI
from fastapi.responses import HTMLResponse
 
import database.session

database.session

app = FastAPI()
 
@app.get("/")
def read_root():
  html_content = "<h2>Hello METANIT.COM!</h2>"
  return HTMLResponse(content=html_content)