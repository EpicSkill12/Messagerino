from sqlite3 import Connection, Cursor, connect
from uuid import UUID
from custom_types.baseTypes import Nachricht, Nutzer, SQLNachricht, SQLNutzer, toNachricht, toNutzer

class Datenbank():
    def __init__(self) -> None:
        self.__connection: Connection = connect("Datenbank.db")
        self.__cursor: Cursor = self.__connection.cursor()

        

    def findNachricht(self, id: UUID) -> Nachricht:
        self.__cursor.execute(
            "SELECT * " \
            "FROM Nachrichten" \
            "WHERE Nachrichten.UUID = ?",
            (id,)
        )
        ergebnis: list[SQLNachricht] = self.__cursor.fetchall()
        return toNachricht(ergebnis[0]) # ! FIXME: Typsicherheit 
    
    def findeNutzer(self, nutzername: str) -> Nutzer:
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer" \
            "WHERE Nutzer.Nutzername = ?",
            (nutzername,)
        )
        ergebnis: list[SQLNutzer] = self.__cursor.fetchall()
        return toNutzer(ergebnis[0]) # ! FIXME: Typsicherheit 
    
    def findeNachrichtenEinesChats(self, absender:Nutzer, empfaenger:Nutzer) -> tuple[list[Nachricht],list[Nachricht]]:
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nachrichten" \
            "WHERE Nachricht.Absender = ?" \
            "AND Nachricht.Empfaenger = ?",
            (absender, empfaenger)
            )
        ergebnis1:list[SQLNachricht] = self.__cursor.fetchall()

        self.__cursor.execute(
            "SELECT *" \
            "FROM Nachrichten" \
            "WHERE Nachricht.Absender = ?" \
            "AND Nachricht.Empfaenger = ?",
            (empfaenger, absender)
        )
        ergebnis2:list[SQLNachricht] = self.__cursor.fetchall()

        return ([toNachricht(element) for element in ergebnis1], [toNachricht(element) for element in ergebnis2])
    
    def getAlleNutzer(self) -> list[Nutzer]:
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer"
        )
        ergebnis:list[SQLNutzer] = self.__cursor.fetchall()
        return [toNutzer(element) for element in ergebnis]
# TODO: ChatAbfrage-Methode

datenbank = Datenbank()