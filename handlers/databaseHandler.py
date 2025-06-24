from sqlite3 import Connection, Cursor, connect
from uuid import UUID
from custom_types.baseTypes import Chat, Message, SQLMessage, SQLUser, TupleMessage, TupleUser
from helpers.conversionHelper import toMessage, toSQLMessage, toSQLUser, toUser
from config.constants import DB_PATH
from typing import Optional

class Database():
    # === INITIALISIERUNG ===
    def __init__(self) -> None:
        self.__connection: Connection = connect(DB_PATH)
        self.__cursor: Cursor = self.__connection.cursor()

        self.setup()

    def setup(self) -> None:
        """
        Vor.: -
        Eff.: Datenbank wird erstellt (falls nicht vorhanden)
        Erg.: -
        """
        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS Nutzer(" \
            "Nutzername TEXT PRIMARY KEY," \
            "Anzeigename TEXT NOT NULL," \
            "PasswortHash TEXT NOT NULL," \
            "Erstellungsdatum REAL NOT NULL" \
            ")"
        )
        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS Nachrichten(" \
            "UUID TEXT PRIMARY KEY," \
            "Absender TEXT NOT NULL," \
            "Empfaenger TEXT NOT NULL," \
            "Inhalt TEXT NOT NULL," \
            "Zeitstempel REAL NOT NULL," \
            "Lesebestaetigung INT NOT NULL" \
            ")"
        )
     
    # === Suche ===
    def findMessage(self, id: UUID) -> Optional[SQLMessage]:
        """
        Vor.: id ist eine UUID einer Nachricht aus der Datenbank
        Eff.: -
        Erg.: Die Nachricht mit der eingegebenen ID wird zurückgegeben
        """
        self.__cursor.execute(
            "SELECT * " \
            "FROM Messages" \
            "WHERE Messages.UUID = ?",
            (id,)
        )
        result: list[TupleMessage] = self.__cursor.fetchall()
        if not result:
            return
        return toSQLMessage(result[0])

    def findUser(self, username: str) -> Optional[SQLUser]:
        """
        Vor.: username ist der Nutzername eines Nutzers in der Datenbank
        Eff.: -
        Erg.: Der Nutzer mit dem eingegebenen Nutzernamen wird zurückgegeben
        """
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer" \
            "WHERE Nutzer.Nutzername = ?",
            (username,)
        )
        result: list[TupleUser] = self.__cursor.fetchall()
        if not result:
            return
        return toSQLUser(result[0])

    def findMessagesByChat(self, senderName:str, receiverName:str) -> tuple[list[SQLMessage],list[SQLMessage]]:
        """
        Vor.: absender und empfaenger haben einen gemeinsamen Chat
        Eff.: -
        Erg.: Tupel der Listen von Nachrichten des gemeinsamen Chats wird zurückgegeben (1.Liste:gesendete Nachrichten, 2.Liste: empfangene Nachrichten)
        """
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nachrichten" \
            "WHERE Nachricht.Absender = ?" \
            "AND Nachricht.Empfaenger = ?",
            (senderName, receiverName)
            )
        result1: list[TupleMessage] = self.__cursor.fetchall()

        self.__cursor.execute(
            "SELECT *" \
            "FROM Nachrichten" \
            "WHERE Nachricht.Absender = ?" \
            "AND Nachricht.Empfaenger = ?",
            (receiverName, senderName) 
        )
        result2: list[TupleMessage] = self.__cursor.fetchall()

        return ([toSQLMessage(element) for element in result1], [toSQLMessage(element) for element in result2])

    def findChatsByUser(self, username: str) -> list[Chat]:
        self.__cursor.execute(
            "SELECT Empfaenger" \
            "FROM Nachrichten" \
            "WHERE Absender = ?" \
            "INTERSECT" \
            "SELECT Absender" \
            "FROM Nachrichten" \
            "WHERE Empfaenger = ?",
            (username,username)
        )
        result: list[str] = self.__cursor.fetchall()
        recipients: list[str] = list(set(result))

        def getLastMessage(user: str, user2: str) -> Message:
            self.__cursor.execute(
                "SELECT *" \
                "FROM Nachrichten" \
                "WHERE Absender = ? AND Empfaenger = ?" \
                "INTERSECT" \
                "SELECT *" \
                "FROM Nachrichten" \
                "WHERE Absender = ? AND Empfaenger = ?" \
                "ORDER BY Zeitstempel DESC",
                (user, user2, user2, user)
            )
            result: list[TupleMessage] = self.__cursor.fetchall()
            return toMessage(toSQLMessage(result[0]))
        
        finalResult:list[Chat] = []
        for recipient in recipients:
            finalResult.append(Chat(recipient = toUser(recipient), lastMessage = getLastMessage(user = username, user2 = recipient)))

        return finalResult

    # === Getter ===
    def getAllUser(self) -> list[SQLUser]:
        """
        Vor.: -
        Eff.: - 
        Erg.: Gibt alle Nutzer zurück
        """
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer"
        )
        result:list[TupleUser] = self.__cursor.fetchall()
        return [toSQLUser(element) for element in result]
    
    # === Setter ===
    def createUser(self, nutzername:str, anzeigename: str, passwortHash: str, erstellungsdatum: float) -> None:
        self.__cursor.execute(
            "SELECT 1 FROM Nutzer WHERE Nutzername = ?",
            (nutzername,)
        )
        if self.__cursor.fetchone():
            pass #TODO: Send error to User!

        self.__cursor.execute(
            "INSERT INTO Nutzer (Nutzername, Anzeigename, PasswortHash, Erstellungsdatum)" \
            "VALUES (?,?,?,?)",
            (nutzername,anzeigename,passwortHash,erstellungsdatum)
        )
        self.__connection.commit()

#========
#= CODE
#========

# TODO: ChatAbfrage-Methode

database = Database()

# def toMessage(sqlMessage: SQLMessage) -> Message:
#     """
#     Vor.: -
#     Eff.: - 
#     Erg.: Liefert die eingegebene SQLNachricht als Objekt der Klasse Nachricht wieder 
#     """
#     return Message(UUID=UUID(sqlMessage["ID"]), senderName=sqlMessage["Sender"], receiverName=sqlMessage["Receiver"], content=sqlMessage["Content"], sendTime=sqlMessage["SendTime"], read=sqlMessage["Read"])

# def toUser(sqlUser: SQLUser) -> User:
#     """
#     Vor.: -
#     Eff.: - 
#     Erg.: Liefert die eingegebene SQLNachricht als Objekt der Klasse Nutzer wieder 
#     """
#     return User(UUID=UUID(sqlUser["ID"]), username=sqlUser["Username"], displayName=sqlUser["DisplayName"])