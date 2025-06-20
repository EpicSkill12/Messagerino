from sqlite3 import Connection, Cursor, connect
from uuid import UUID
from types.baseTypes import Message, User, SQLMessage, SQLUser, toMessage, toUser

class Database():
    def __init__(self) -> None:
        self.__connection: Connection = connect("database.db")
        self.__cursor: Cursor = self.__connection.cursor()

    def findMessage(self, ID: UUID) -> Message:
        self.__cursor.execute(
            "SELECT * " \
            "FROM Messages" \
            "WHERE Messages.UUID = ?",
            (ID,)
        )
        result: list[SQLMessage] = self.__cursor.fetchall()
        return toMessage(result[0]) # ! FIXME: Typsicherheit 
    
    def findUser(self, Username: str) -> User:
        self.__cursor.execute(
            "SELECT *" \
            "FROM User" \
            "WHERE User.Username = ?",
            (Username,)
        )
        result: list[SQLUser] = self.__cursor.fetchall()
        return toUser(result[0]) # ! FIXME: Typsicherheit 
    
# TODO: ChatAbfrage-Methode

database = Database()