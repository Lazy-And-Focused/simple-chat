from database.schemas import AuthBase, UserBase
from database.session import Database

import hash

def fetch(token: str):
    hash = token.split(":")[0]
    data = Database(AuthBase).getByKey("hash", hash)
    
    return data[0]

def fetchUser(token: str) -> tuple[AuthBase, UserBase]:
    auth = fetch(token)
    user = Database(UserBase).getById(auth.user_id)

    return auth, user

def generateToken(user_id: int, email: str, password: str):
    email_hash = hash.createHash(email).hex()
    return email_hash, f"{email_hash}:{hash.createHash(f"{email}{password}{user_id}").hex()}"

def validate(token: str|None):
    if token == None:
        return False
    
    splitted_token = token.split(":")

    if len(splitted_token) != 2:
        return False
    
    hash = splitted_token[0]
    data = Database(AuthBase).getByKey("hash", hash)

    if len(data) == 0:
        return False
    
    if data[0].access_token != token:
        return False
    
    return True