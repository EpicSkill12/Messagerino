from hashlib import sha256
import secrets

def hashPW(password: str) -> str:
    return sha256(password.encode("UTF-8")).hexdigest()

def getBaseModulusAndSecret(bits: int = 1024) -> tuple[int, int, int]:
    def generateSafePrime(bits: int):
        def isPrime(n: int, k: int = 40):
            if n < 2:
                return False
            small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
            for sp in small_primes:
                if n == sp:
                    return True
                if n % sp == 0:
                    return False
            r, d = 0, n - 1
            while d % 2 == 0:
                r += 1
                d //= 2
            for _ in range(k):
                a = secrets.randbelow(n - 3) + 2
                x = pow(a, d, n)
                if x in (1, n - 1):
                    continue
                for _ in range(r - 1):
                    x = pow(x, 2, n)
                    if x == n - 1:
                        break
                else:
                    return False
            return True
        
        def generatePrime(bits: int):
            while True:
                candidate = secrets.randbits(bits) | (1 << bits - 1) | 1
                if isPrime(candidate):
                    return candidate
        
        qBits = bits - 1
        while True:
            q: int = generatePrime(qBits)
            p: int = 2 * q + 1
            if isPrime(p):
                return p, q
        
    def getBase(p: int, q: int):
        while True:
            h = secrets.randbelow(p - 3) + 2
            g = pow(h, 2, p)
            if g != 1 and pow(g, q, p) != 1:
                return g
    
    p, q = generateSafePrime(bits)
    b = getBase(p, q)
    secret = secrets.randbelow(p - 3) + 2
    return (b, p, secret)