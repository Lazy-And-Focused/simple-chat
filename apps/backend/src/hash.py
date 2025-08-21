import hashlib

import env

def createHash(data: str):
    return hashlib.sha256(f"{env.get("HASH_KEY")}{data}".encode()).digest()

def hashFromBytes(salt: bytes, data: str):
    hashed = hashlib.pbkdf2_hmac(
        "sha512",
        data.encode("utf-8"),
        salt,
        50000,
        dklen=256
    )

    return f"{salt.hex()}:{hashed.hex()}"

def hash(key: str, data: str):
    salt = createHash(key)

    return hashFromBytes(salt, data)

def resolveHash(hash: str):
    salt, data = hash.split(":")

    return b"".fromhex(salt), data

def isHashEquals(hashed: str, data: str):
    salt, _ = resolveHash(hashed)
    
    return hashed == hashFromBytes(salt, data)

def isKeyEquals(key: str, hashed: str):
    salt, _ = resolveHash(hashed)

    if salt == createHash(key):
        return True
    else:
        return False
    
def changeHash(key: str, data: str, hashed: str):
    if (not isKeyEquals(key, hashed)): return False
     
    salt, _ = resolveHash(hashed)

    return hashFromBytes(salt, data)

def changeKey(newKey: str, oldKey: str, data: str, hashed: str):
    oldSalt, _ = resolveHash(hashed)
    
    if (oldSalt != createHash(oldKey)): return False

    return hash(newKey, data)

def main():
    password = hash("someemail@some.example", "my cool password")
    
    print("password:", password)
    print("isHashEquals:", isHashEquals(password, "my cool password"))
    print("isKeyEquals:", isKeyEquals("someemail@some.example", password))
    print("changeHash:", changeHash("someemail@some.example", "my new cool password", password))
    print("changeKey:", changeKey("123", "someemail@some.example", "my cool password", password))

if __name__ == "__main__":
    main()