from typing import TypedDict
import uuid
from handlers.databaseHandler import database

class SQLMessage(TypedDict):
    ID: str
    Sender: str
    Receiver: str
    Content: str
    SendTime: float
    Read: bool

class SQLUser(TypedDict):
    ID: str
    Username: str
    DisplayName: str

class Message():
    def __init__(self, UUID:uuid.UUID, sender:"User", receiver: "User", content: str, sendTime:float, read: bool) -> None:
        
        self.__UUID = UUID
        self.__sender = sender
        self.__receiver = receiver
        self.__content = content
        self.__sendTime = sendTime
        self.__read = read
    
    # *Getter
    def getUUID(self) -> uuid.UUID:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt die UUID der Nachricht zurück
        """
        return self.__UUID
    def getAbsender(self) -> "User":
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Absender der Nachricht zurück
        """
        return self.__absender
    def getEmpfaenger(self) -> "User":
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Empfaenger der Nachricht zurück
        """
        return self.__empfaenger
    def getInhalt(self) -> str:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Inhalt (Text) der Nachricht zurück
        """
        return self.__inhalt
    def getZeitstempel(self) -> float:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Zeitstempel der Nachricht zurück
        """
        return self.__zeitstempel
    def getLesebestaetigung(self) -> bool:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Status der Lesebestaetigung der Nachricht zurück
        """
        return self.__lesebestaetigung
    
    # *Methoden
    def toDict(self) -> SQLMessage:
        """
        Vor.: -
        Eff.: - 
        Erg.: Liefert die Nachricht, als SQLNachricht
        """
        return {
            "ID": str(self.__UUID),
            "Sender": str(self.__sender.getUUID()),
            "Receiver": str(self.__receiver.getUUID()),
            "Content":  self.__content,
            "SendTime": self.__sendTime,
            "Read": self.__read
        }

class User():
    def __init__(self, UUID: uuid.UUID, username: str, displayName: str) -> None:
        self.__UUID = UUID
        self.__username = username
        self.__displayName = displayName
    
    # *Getter
    def getUUID(self) -> uuid.UUID:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt die UUID des Nutzers zurück
        """
        return self.__UUID
    
    def getUsername(self) -> str:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Nutzername des Nutzers zurück
        """
        return self.__username
    
    def getDisplayName(self) -> str:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Anzeigenamen des Nutzers zurück
        """
        return self.__displayName
    
    # *Methoden
    def toDict(self) -> SQLUser:
        """
        Vor.: -
        Eff.: - 
        Erg.: Liefert den Nutzer, als SQLNachricht
        """
        return {
            "ID": str(self.__UUID),
            "Username": self.__username,
            "DisplayName": self.__displayName
        }

def toMessage(sqlMessage: SQLMessage) -> Message:

    return Message(UUID=uuid.UUID(sqlMessage["ID"]), sender = database.findUser(sqlMessage["Sender"]), receiver = database.findUser(sqlMessage["Receiver"]), content = sqlMessage["Content"], sendTime = sqlMessage["SendTime"], read = sqlMessage["Read"])

def toUser(sqlUser: SQLUser) -> User:
    
    return User(UUID = uuid.UUID(sqlUser["ID"]), username = sqlUser["Username"], displayName = sqlUser["DisplayName"])

# a = User(UUID=uuid.uuid1(7), username="Frank", displayName="Fränki")
# x = Message(UUID=uuid.uuid1(3), sender=a, receiver=a, content="Hallo", sendTime=389768.378, read=True)