import hashlib
def hash_string(input_string: str) -> str:
    """Generate a SHA-256 hash of the input string."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

def check_hash(input_string: str, expected_hash: str = "0d5d680cb2f86f4a4bcbfa7bf6ef65aba1947d2c09d6a56f7548d42a5c369a25") -> bool:
    """Check if the SHA-256 hash of the input string matches the expected hash."""
    return hash_string(input_string) == expected_hash
print(check_hash("MeinPasswort1"))


