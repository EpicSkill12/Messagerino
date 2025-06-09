from sqlite3 import Connection, Cursor, connect
from uuid import UUID
from types.baseTypes import Nachricht, SQLNachricht, toNachricht

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
        return toNachricht(ergebnis[0])
    
# TODO: ChatAbfrage-Methode