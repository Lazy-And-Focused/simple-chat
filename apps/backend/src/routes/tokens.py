from database.schemas import AuthBase, UserBase
from database.session import Database

import hash

def fetch(token: str):
    hash = token.split(":")[0]
    data = Database(AuthBase).getByKey("hash", hash)
    
    return data[0]

def fetchUser(token: str):
    auth = fetch(token)
    user = Database(UserBase).getById(auth.user_id)

    return auth, user

def generateToken(userId: int, email: str, password: str):
    emailHash = hash.createHash(email).hex()
    return emailHash, f"{emailHash}:{hash.createHash(f"{email}{password}{userId}").hex()}"

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