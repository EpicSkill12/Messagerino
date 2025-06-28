from hashlib import sha256
import secrets
from Crypto.Util import number

def hashPW(password: str) -> str:
    return sha256(password.encode("UTF-8")).hexdigest()

def makeKey(p: int) -> int:
    return secrets.randbelow(p - 3) + 2

def generateSafePrime(bits: int) -> tuple[int, int]:
    while True:
        q = number.getPrime(bits - 1) # type: ignore
        p = 2 * q + 1
        if number.isPrime(p): # type: ignore
            return p, q

def getBase(p: int, q: int) -> int:
    while True:
        h = secrets.randbelow(p - 3) + 2
        g = pow(h, (p - 1) // q, p)
        if g > 1 and pow(g, q, p) == 1:
            return g

def getBaseModulusAndSecret(bits: int = 1024) -> tuple[int, int, int]:
    p, q = generateSafePrime(bits)
    b = getBase(p, q)
    secret = makeKey(p)
    return b, p, secret

if __name__ == "__main__":
    b, m, s = getBaseModulusAndSecret()
    print(b, m, s)
