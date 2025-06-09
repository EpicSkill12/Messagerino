from sqlite3 import Connection, Cursor, connect
from uuid import UUID
from custom_types.baseTypes import Nachricht, Nutzer, SQLNachricht, SQLNutzer
from config.constants import DB_PATH
import os

class Datenbank():
    def __init__(self) -> None:
        self.__connection: Connection = connect(DB_PATH)
        self.__cursor: Cursor = self.__connection.cursor()

        if os.path.exists(DB_PATH):
            return

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

def toNachricht(sqlNachricht: SQLNachricht) -> Nachricht:
    return Nachricht(UUID=UUID(sqlNachricht["ID"]), absender = datenbank.findeNutzer(sqlNachricht["Absender"]), empfaenger = datenbank.findeNutzer(sqlNachricht["Empfaenger"]), inhalt = sqlNachricht["Inhalt"], zeitstempel = sqlNachricht["Zeitstempel"], lesebestaetigung = sqlNachricht["Lesebestaetigung"])

def toNutzer(sqlNutzer: SQLNutzer) -> Nutzer:
    return Nutzer(UUID = UUID(sqlNutzer["ID"]), nutzername = sqlNutzer["Nutzername"], anzeigename = sqlNutzer["Anzeigename"])