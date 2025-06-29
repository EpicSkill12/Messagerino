from custom_types.baseTypes import SQLMessage, SQLUser, TupleMessage, TupleUser, User

#=========
#= ZU SQL
#=========

def toSQLUser(tupleUser: TupleUser) -> SQLUser:
    username, displayName, passwordHash, creationDate = tupleUser
    return {"Username": username, "DisplayName": displayName, "PasswordHash": passwordHash, "CreationDate": creationDate}

def toSQLMessage(tupleMessage: TupleMessage) -> SQLMessage:
    _id, sender, receiver, content, sendTime, read = tupleMessage
    return {"ID": _id, "Sender": sender, "Receiver": receiver, "Content": content, "SendTime": sendTime, "Read": read}

def toSQLUserFromPython(user: User) -> SQLUser:
    return {"Username": user.getUsername(), "DisplayName": user.getDisplayName(), "CreationDate": user.getCreationDate(), "PasswordHash": user.getPasswordHash()}
