from sqlite3 import Connection, Cursor, connect
from uuid import UUID
from types.baseTypes import Nachricht, Nutzer, SQLNachricht, SQLNutzer, toNachricht, toNutzer

class Datenbank():
    def __init__(self) -> None:
        self.__connection: Connection = connect("Datenbank.db")
        self.__cursor: Cursor = self.__connection.cursor()

    def findNachricht(self, ID: UUID) -> Nachricht:
        self.__cursor.execute(
            "SELECT * " \
            "FROM Nachrichten" \
            "WHERE Nachrichten.UUID = ?",
            (ID,)
        )
        ergebnis: list[SQLNachricht] = self.__cursor.fetchall()
        return toNachricht(ergebnis[0]) # ! FIXME: Typsicherheit 
    
    def findeNutzer(self, Nutzername: str) -> Nutzer:
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer" \
            "WHERE Nutzer.Nutzername = ?",
            (Nutzername,)
        )
        ergebnis: list[SQLNutzer] = self.__cursor.fetchall()
        return toNutzer(ergebnis[0]) # ! FIXME: Typsicherheit 
    
# TODO: ChatAbfrage-Methode

datenbank = Datenbank()