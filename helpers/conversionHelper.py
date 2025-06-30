from custom_types.baseTypes import SQLMessage, SQLUser, TupleMessage, TupleUser, User

#=========
#= ZU SQL
#=========

def toSQLUser(tupleUser: TupleUser) -> SQLUser:
    """
    Vor.: tupleUser ist ein Tupel eines SQL Users
    Eff.: -
    Erg.: Gibt ein SQLUser-Dictionary zurück
    """
    username, displayName, passwordHash, creationDate = tupleUser
    return {"Username": username, "DisplayName": displayName, "PasswordHash": passwordHash, "CreationDate": creationDate}

def toSQLMessage(tupleMessage: TupleMessage) -> SQLMessage:
    """
    Vor.: tupleMessage ist ein Tupel einer SQL Nachricht
    Eff.: -
    Erg.: Gibt ein SQLMessage-Dictionary zurück
    """
    _id, sender, receiver, content, sendTime, read = tupleMessage
    return {"ID": _id, "Sender": sender, "Receiver": receiver, "Content": content, "SendTime": sendTime, "Read": read}

def toSQLUserFromPython(user: User) -> SQLUser:
    """
    Vor.: user ist ein Python User Objekt
    Eff.: -
    Erg.: Gibt ein SQLUser-Dictionary zurück
    """
    return {"Username": user.getUsername(), "DisplayName": user.getDisplayName(), "CreationDate": user.getCreationDate(), "PasswordHash": user.getPasswordHash()}
