import hashlib
def hash_string(input_string: str) -> str:
    """Generate a SHA-256 hash of the input string."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

def check_hash(input_string: str, expected_hash: str = "b1ad66d9501eae4bbef7a24e9ac888fbfea9c43c557645d0a6995a01b5eecd5a") -> bool:
    """Check if the SHA-256 hash of the input string matches the expected hash."""
    return hash_string(input_string) == expected_hash


print(check_hash("HalloWelt!"))


