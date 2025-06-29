import uuid
from custom_types.baseTypes import Message, SQLMessage, SQLUser, TupleMessage, TupleUser, User
from typing import Union

import requests

#=========
#= ZU SQL
#=========

def toSQLUser(tupleUser: TupleUser) -> SQLUser:
    username, displayName, passwordHash, creationDate = tupleUser
    return {"Username": username, "DisplayName": displayName, "PasswordHash": passwordHash, "CreationDate": creationDate}

def toSQLMessage(tupleMessage: TupleMessage) -> SQLMessage:
    _id, sender, receiver, content, sendTime, read = tupleMessage
    return {"ID": _id, "Sender": sender, "Receiver": receiver, "Content": content, "SendTime": sendTime, "Read": read} # ! FIXME: Typsicherheit 

def toSQLUserFromPython(user: User) -> SQLUser:
    return {"Username": user.getUsername(), "DisplayName": user.getDisplayName(), "CreationDate": user.getCreationDate(), "PasswordHash": user.getPasswordHash()}

#============
#= ZU PYTHON
#============

def toUser(sqlUser: Union[SQLUser, str]) -> User:
    if isinstance(sqlUser, dict):
        return User(username = sqlUser["Username"], displayName = sqlUser["DisplayName"], passwordHash=sqlUser["PasswordHash"], creationDate=sqlUser["CreationDate"])
    
    else:
        try:
            response = requests.get("http://127.0.0.1:5000/user", params = {"name": sqlUser})
            if response.status_code == 200:
                data = response.json()
                return User(
                    username = data["Username"],
                    displayName = data["DisplayName"],
                    passwordHash = data["PasswordHash"],
                    creationDate = data["CreationDate"]
                )
            else:
                raise ValueError(f"Benutzer '{sqlUser}' nicht gefunden. Serverantwort: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Verbindung zum Server fehlgeschlagen: {e}")
        
def toMessage(sqlMessage: SQLMessage) -> Message:
    return Message(UUID=uuid.UUID(sqlMessage["ID"]), sender = toUser(sqlMessage["Sender"]), receiver = toUser(sqlMessage["Receiver"]), content = sqlMessage["Content"], sendTime = sqlMessage["SendTime"], read = sqlMessage["Read"])
