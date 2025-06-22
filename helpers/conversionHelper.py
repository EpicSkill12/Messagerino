import uuid
from custom_types.baseTypes import User, SQLUser, SQLMessage, Message
from typing import Union

import requests

def toUser(sqlUser: Union[SQLUser, str]) -> User:
    if isinstance(sqlUser, dict):
        return User(username = sqlUser["Username"], displayName = sqlUser["DisplayName"], passwordHash=sqlUser["PasswordHash"], creationDay=sqlUser["CreationDay"])
    
    else:
        try:
            response = requests.get("http://127.0.0.1:5000/user", params = {"name": sqlUser})
            if response.status_code == 200:
                data = response.json()
                return User(
                    username = data["Username"],
                    displayName = data["DisplayName"],
                    passwordHash = data["PasswordHash"],
                    creationDay = data["CreationDay"]
                )
            else:
                raise ValueError(f"Benutzer '{sqlUser}' nicht gefunden. Serverantwort: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Verbindung zum Server fehlgeschlagen: {e}")
        
def toMessage(sqlMessage: SQLMessage) -> Message:
    # TODO: make request to get actual Users instead of names only
    return Message(UUID=uuid.UUID(sqlMessage["ID"]), sender = toUser(sqlMessage["Sender"]), receiver = toUser(sqlMessage["Receiver"]), content = sqlMessage["Content"], sendTime = sqlMessage["SendTime"], read = sqlMessage["Read"])


