from sqlite3 import Connection, Cursor, connect
from uuid import UUID
from custom_types.baseTypes import Message, User, SQLMessage, SQLUser
from config.constants import DB_PATH

class Database():
    def __init__(self) -> None:
        self.__connection: Connection = connect(DB_PATH)
        self.__cursor: Cursor = self.__connection.cursor()

        self.setup()

    
    
    # * Getter
    
    
    
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
    def findNachricht(self, id: UUID) -> Message:
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
        result: list[SQLMessage] = self.__cursor.fetchall()
        return toMessage(result[0]) # ! FIXME: Typsicherheit 
    
    def findUser(self, username: str) -> User:
        """
        Vor.: username ist der Nutzername eines Nutzers in der Datenbank
        Eff.: -
        Erg.: Der Nutzer mit dem eingegebenen Nutzernamen wird zurückgegeben
        """
    def findUser(self, username: str) -> User:
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer" \
            "WHERE Nutzer.Nutzername = ?",
            (username,)
        )
        ergebnis: list[SQLUser] = self.__cursor.fetchall()
        return toNutzer(ergebnis[0]) # ! FIXME: Typsicherheit 
    
    def findeNachrichtenEinesChats(self, absender:User, empfaenger:User) -> tuple[list[Message],list[Message]]:
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
            (absender, empfaenger)
            )
        ergebnis1:list[SQLMessage] = self.__cursor.fetchall()

        self.__cursor.execute(
            "SELECT *" \
            "FROM Nachrichten" \
            "WHERE Nachricht.Absender = ?" \
            "AND Nachricht.Empfaenger = ?",
            (empfaenger, absender)
        )
        ergebnis2:list[SQLMessage] = self.__cursor.fetchall()

        return ([toMessage(element) for element in ergebnis1], [toMessage(element) for element in ergebnis2])

    def getAlleNutzer(self) -> list[User]:
        """
        Vor.: -
        Eff.: - 
        Erg.: Gibt alle Nutzer zurück
        """
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer"
        )
        ergebnis:list[SQLUser] = self.__cursor.fetchall()
        return [toNutzer(element) for element in ergebnis]
    

# TODO: ChatAbfrage-Methode

database = Database()

def toMessage(sqlMessage: SQLMessage) -> Message:
    """
    Vor.: -
    Eff.: - 
    Erg.: Liefert die eingegebene SQLNachricht als Objekt der Klasse Nachricht wieder 
    """
    return Message(UUID=UUID(sqlMessage["ID"]), sender=database.findUser(sqlMessage["Sender"]), receiver=database.findUser(sqlMessage["Receiver"]), content=sqlMessage["Content"], sendTime=sqlMessage["SendTime"], read=sqlMessage["Read"])

def toNutzer(sqlNutzer: SQLUser) -> User:
    """
    Vor.: -
    Eff.: - 
    Erg.: Liefert die eingegebene SQLNachricht als Objekt der Klasse Nutzer wieder 
    """
    return User(UUID=UUID(sqlNutzer["ID"]), username=sqlNutzer["Nutzername"], displayName=sqlNutzer["Anzeigename"])