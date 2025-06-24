from hashlib import sha256

def hashPW(password: str) -> str:
    return sha256(password.encode("UTF-8")).hexdigest()

