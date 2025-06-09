from typing import TypedDict
import uuid
from handlers.databaseHandler import datenbank

class SQLNachricht(TypedDict):
    ID: str
    Absender: str
    Empfaenger: str
    Inhalt: str
    Zeitstempel: float
    Lesebestaetigung: bool

class SQLNutzer(TypedDict):
    ID: str
    Nutzername: str
    Anzeigename: str

class Nachricht():
    def __init__(self, UUID:uuid.UUID, absender:"Nutzer", empfaenger: "Nutzer", inhalt: str, zeitstempel:float, lesebestaetigung: bool) -> None:
        
        self.__UUID = UUID
        self.__absender = absender
        self.__empfaenger = empfaenger
        self.__inhalt = inhalt
        self.__zeitstempel = zeitstempel
        self.__lesebestaetigung = lesebestaetigung
    
    # *Getter
    def getUUID(self) -> uuid.UUID:
        return self.__UUID
    def getAbsender(self) -> "Nutzer":
        return self.__absender
    def getEmpfaenger(self) -> "Nutzer":
        return self.__empfaenger
    def getInhalt(self) -> str:
        return self.__inhalt
    def getZeitstempel(self) -> float:
        return self.__zeitstempel
    def getLesebestaetigung(self) -> bool:
        return self.__lesebestaetigung
    
    # *Methoden
    def toDict(self) -> SQLNachricht:
        return {
            "ID": str(self.__UUID),
            "Absender": str(self.__absender.getUUID()),
            "Empfaenger": str(self.__empfaenger.getUUID()),
            "Inhalt":  self.__inhalt,
            "Zeitstempel": self.__zeitstempel,
            "Lesebestaetigung": self.__lesebestaetigung
        }

class Nutzer():
    def __init__(self, UUID: uuid.UUID, nutzername: str, anzeigename: str) -> None:
        self.__UUID = UUID
        self.__nutzername = nutzername
        self.__anzeigename = anzeigename
    
    # *Getter
    def getUUID(self) -> uuid.UUID:
        return self.__UUID
    
    def getNutzername(self) -> str:
        return self.__nutzername
    
    def getAnzeigename(self) -> str:
        return self.__anzeigename
    
    # *Methoden
    def toDict(self) -> SQLNutzer:
        return {
            "ID": str(self.__UUID),
            "Nutzername": self.__nutzername,
            "Anzeigename": self.__anzeigename
        }

def toNachricht(sqlNachricht: SQLNachricht) -> Nachricht:

    return Nachricht(UUID=uuid.UUID(sqlNachricht["ID"]), absender = datenbank.findeNutzer(sqlNachricht["Absender"]), empfaenger = datenbank.findeNutzer(sqlNachricht["Empfaenger"]), inhalt = sqlNachricht["Inhalt"], zeitstempel = sqlNachricht["Zeitstempel"], lesebestaetigung = sqlNachricht["Lesebestaetigung"])

def toNutzer(sqlNutzer: SQLNutzer) -> Nutzer:
    
    return Nutzer(UUID = uuid.UUID(sqlNutzer["ID"]), nutzername = sqlNutzer["Nutzername"], anzeigename = sqlNutzer["Anzeigename"])

# a = Nutzer(UUID=uuid.uuid1(7), nutzername="Frank", anzeigename="Fränki")
# x = Nachricht(UUID=uuid.uuid1(3), absender=a, empfaenger=a, inhalt="Hallo", zeitstempel=389768.378, lesebestaetigung=True)