from Messagerino.custom_types.httpTypes import HTTP
from flask import Response
from typing import TypedDict
import uuid
from Messagerino.helpers.formattingHelper import makeResponse

#==========
#= NETZWERK
#==========

class Result:
    def __init__(self, success: bool = False, message: str = "", code: HTTP = HTTP.OK):
        self.success = success
        self.message = message
        self.code = code
    def toResponse(self, encryptionKey: int | None = None) -> Response:
        return makeResponse(obj={"message": self.message}, code=self.code, encryptionKey = encryptionKey)

#=======
#= SQL
#=======

class SQLMessage(TypedDict):
    ID: str
    Sender: str
    Receiver: str
    Content: str
    SendTime: float
    Read: bool

class SQLUser(TypedDict):
    Username: str
    DisplayName: str
    PasswordHash: str
    CreationDate: float

class SQLChat(TypedDict):
    Recipient: str
    LastMessage: SQLMessage

#========
#= Tupel
#========

TupleMessage = tuple[str, str, str, str, float, bool]

TupleUser = tuple[str, str, str, float]

TupleChat = tuple[str, TupleMessage]

#==========
#= Python
#==========

class Message():
    def __init__(self, UUID:uuid.UUID, sender: "User", receiver: "User", content: str, sendTime:float, read: bool) -> None:
        
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
    def getSender(self) -> "User":
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Absender der Nachricht zurück
        """
        return self.__sender
    def getReceiver(self) -> "User":
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Empfaenger der Nachricht zurück
        """
        return self.__receiver
    def getContent(self) -> str:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Inhalt (Text) der Nachricht zurück
        """
        return self.__content
    def getSendTime(self) -> float:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Zeitstempel der Nachricht zurück
        """
        return self.__sendTime
    def getReadStatus(self) -> bool:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Status der Lesebestaetigung der Nachricht zurück
        """
        return self.__read
    
    # *Methoden
    def toDict(self) -> SQLMessage:
        """
        Vor.: -
        Eff.: - 
        Erg.: Liefert die Nachricht, als SQLNachricht
        """
        return {
            "ID": str(self.__UUID),
            "Sender": self.__sender.getUsername(),
            "Receiver": self.__receiver.getUsername(),
            "Content":  self.__content,
            "SendTime": self.__sendTime,
            "Read": self.__read
        }

class User():
    def __init__(self, username: str, displayName: str, passwordHash: str, creationDate: float) -> None:
        self.__username = username
        self.__displayName = displayName
        self.__passwordHash = passwordHash
        self.__creationDate = creationDate
    
    # *Getter
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
    
    def getPasswordHash(self) -> str:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den PasswortHash des Nutzers zurück
        """
        return self.__passwordHash
    
    def getCreationDate(self) -> float:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Erstellungszeitpunkt des Nutzers zurück
        """
        return self.__creationDate
    
    # *Methoden
    def toDict(self) -> SQLUser:
        """
        Vor.: -
        Eff.: - 
        Erg.: Liefert den Nutzer, als SQLNachricht
        """
        return {
            "Username": self.__username,
            "DisplayName": self.__displayName,
            "PasswordHash": self.__passwordHash,
            "CreationDate": self.__creationDate
        }

class Chat():
    def __init__(self, recipient: User, lastMessage: Message) -> None:
        self.__recipient = recipient
        self.__lastMessage = lastMessage
    
    def getRecipient(self) -> User:
        return self.__recipient
    def getLastMessage(self) -> Message:
        return self.__lastMessage


#========
#= JSON
#========

class JsonChat(TypedDict):
    Recipient: SQLUser
    LastMessage: SQLMessage