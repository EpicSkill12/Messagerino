import hashlib
def hash_string(input_string: str) -> str:
    """
    Vor.: input_string ist ein String
    Eff.: -
    Erg.: Gibt den SHA-256 Hash des Strings zurück
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

def check_hash(input_string: str, expected_hash: str = "b1ad66d9501eae4bbef7a24e9ac888fbfea9c43c557645d0a6995a01b5eecd5a") -> bool:
    """
    Vor.: input_string ist ein String, expected_hash ein gültiger Hash
    Eff.: -
    Erg.: True, falls Hash übereinstimmt
    """
    return hash_string(input_string) == expected_hash


print(check_hash("HalloWelt!"))


