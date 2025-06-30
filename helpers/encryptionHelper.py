from typing import Any
import json
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import secrets
from Crypto.Util import number

def hashPW(password: str) -> str:
    """
    Vor.: password ist ein String
    Eff.: -
    Erg.: Gibt den SHA-256 Hash des Passworts zurück
    """
    return sha256(password.encode("UTF-8")).hexdigest()

def makeKey(p: int) -> int:
    """
    Vor.: p ist eine Primzahl
    Eff.: -
    Erg.: Gibt eine zufällige Zahl im Intervall [2, p-1]
    """
    return secrets.randbelow(p - 3) + 2

def getBase(p: int, q: int) -> int:
    """
    Vor.: p und q sind Primzahlen
    Eff.: -
    Erg.: Liefert eine passende Basis für das Diffie-Hellman-Verfahren
    """
    while True:
        h = secrets.randbelow(p - 3) + 2
        g = pow(h, (p - 1) // q, p)
        if g > 1 and pow(g, q, p) == 1:
            return g

def getBaseModulusAndSecret(bits: int = 1024) -> tuple[int, int, int]:
    """
    Vor.: bits bestimmt die Länge der Primzahl
    Eff.: Generiert Basis, Primzahl und Geheimzahl
    Erg.: Gibt ein Tupel (Basis, Primzahl, Geheimzahl) zurück
    """
    p = number.getStrongPrime(bits) # type: ignore
    q = (p - 1) // 2
    b = getBase(p, q)
    secret = makeKey(p)
    return b, p, secret

# =============

def getKeyFromInt(integer: int) -> bytes:
    """
    Vor.: integer ist ein beliebig großer Integer
    Eff.: -
    Erg.: Liefert einen 32-Byte-Schlüssel
    """
    _bytes = integer.to_bytes((integer.bit_length() + 7) // 8 or 1)
    return hashlib.sha256(_bytes).digest()

def encryptJson(obj: dict[str, Any], integer: int) -> bytes:
    """
    Vor.: obj ist ein Dictionary, integer ist der Schlüssel
    Eff.: Verschlüsselt das Dictionary symmetrisch
    Erg.: Gibt den Ciphertext als Bytes zurück
    """
    key = getKeyFromInt(integer)
    data = json.dumps(obj).encode('utf-8')

    nonce = os.urandom(12)

    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce),
        backend=default_backend()
    ).encryptor()
    ciphertext = cipher.update(data) + cipher.finalize()

    return nonce + cipher.tag + ciphertext

def decryptJson(cipherBlob: bytes, integer: int) -> dict[str, Any]:
    """
    Vor.: cipherBlob wurde mit encryptJson erzeugt
    Eff.: Entschlüsselt den Blob
    Erg.: Gibt das ursprüngliche Dictionary zurück
    """
    key = getKeyFromInt(integer)
    nonce = cipherBlob[:12]
    tag = cipherBlob[12:28]
    ct = cipherBlob[28:]
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce, tag),
        backend=default_backend()
    ).decryptor()
    data = cipher.update(ct) + cipher.finalize()
    return json.loads(data.decode('utf-8'))