from typing import Any
import json
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def getKeyFromInt(integer: int) -> bytes:
    _bytes = integer.to_bytes((integer.bit_length() + 7) // 8 or 1)
    return hashlib.sha256(_bytes).digest()

def encryptJson(obj: dict[str, Any], integer: int) -> bytes:
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