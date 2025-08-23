from database.schemas import AuthBase
from database.session import Database

def fetch(token: str):
    hash = token.split(":")[0]
    data = Database(AuthBase).getByKey("hash", hash)
    
    return data[0]

def validate(token: str|None):
    if token == None:
        return False
    
    splittedToken = token.split(":")

    if len(splittedToken) != 2:
        return False
    
    hash = splittedToken[0]

    data = Database(AuthBase).getByKey("hash", hash)

    if len(data) == 0:
        return False
    
    if data[0].access_token != token:
        return False
    
    return True