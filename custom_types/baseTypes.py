from typing import TypedDict
import uuid

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
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt die UUID der Nachricht zurück
        """
        return self.__UUID
    def getAbsender(self) -> "Nutzer":
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Absender der Nachricht zurück
        """
        return self.__absender
    def getEmpfaenger(self) -> "Nutzer":
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
    def toDict(self) -> SQLNachricht:
        """
        Vor.: -
        Eff.: - 
        Erg.: Liefert die Nachricht, als SQLNachricht
        """
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
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt die UUID des Nutzers zurück
        """
        return self.__UUID
    
    def getNutzername(self) -> str:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Nutzername des Nutzers zurück
        """
        return self.__nutzername
    
    def getAnzeigename(self) -> str:
        """
        Vor.: -
        Eff.: -
        Erg.: Gibt den Anzeigenamen des Nutzers zurück
        """
        return self.__anzeigename
    
    # *Methoden
    def toDict(self) -> SQLNutzer:
        """
        Vor.: -
        Eff.: - 
        Erg.: Liefert den Nutzer, als SQLNachricht
        """
        return {
            "ID": str(self.__UUID),
            "Nutzername": self.__nutzername,
            "Anzeigename": self.__anzeigename
        }

# a = Nutzer(UUID=uuid.uuid1(7), nutzername="Frank", anzeigename="Fraenki")
# x = Nachricht(UUID=uuid.uuid1(3), absender=a, empfaenger=a, inhalt="Hallo", zeitstempel=389768.378, lesebestaetigung=True)