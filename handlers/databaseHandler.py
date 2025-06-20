from sqlite3 import Connection, Cursor, connect
from uuid import UUID
from custom_types.baseTypes import Nachricht, Nutzer, SQLNachricht, SQLNutzer
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
    def findNachricht(self, id: UUID) -> Nachricht:
        """
        Vor.: id ist eine UUID einer Nachricht aus der Datenbank
        Eff.: -
        Erg.: Die Nachricht mit der eingegebenen ID wird zurückgegeben
        """
        self.__cursor.execute(
            "SELECT * " \
            "FROM Nachrichten" \
            "WHERE Nachrichten.UUID = ?",
            (id,)
        )
        result: list[SQLMessage] = self.__cursor.fetchall()
        return toMessage(result[0]) # ! FIXME: Typsicherheit 
    
    def findeNutzer(self, nutzername: str) -> Nutzer:
        """
        Vor.: nutzername ist der Nutzername eines Nutzers in der Datenbank
        Eff.: -
        Erg.: Der Nutzer mit dem eingegebenen Nutzernamen wird zurückgegeben
        """
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer" \
            "WHERE Nutzer.Nutzername = ?",
            (nutzername,)
        )
        ergebnis: list[SQLNutzer] = self.__cursor.fetchall()
        return toNutzer(ergebnis[0]) # ! FIXME: Typsicherheit 
    
    def findeNachrichtenEinesChats(self, absender:Nutzer, empfaenger:Nutzer) -> tuple[list[Nachricht],list[Nachricht]]:
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
        """
        Vor.: -
        Eff.: - 
        Erg.: Gibt alle Nutzer zurück
        """
        self.__cursor.execute(
            "SELECT *" \
            "FROM Nutzer"
        )
        ergebnis:list[SQLNutzer] = self.__cursor.fetchall()
        return [toNutzer(element) for element in ergebnis]
    

# TODO: ChatAbfrage-Methode

datenbank = Datenbank()

def toNachricht(sqlNachricht: SQLNachricht) -> Nachricht:
    """
    Vor.: -
    Eff.: - 
    Erg.: Liefert die eingegebene SQLNachricht als Objekt der Klasse Nachricht wieder 
    """
    return Nachricht(UUID=UUID(sqlNachricht["ID"]), absender = datenbank.findeNutzer(sqlNachricht["Absender"]), empfaenger = datenbank.findeNutzer(sqlNachricht["Empfaenger"]), inhalt = sqlNachricht["Inhalt"], zeitstempel = sqlNachricht["Zeitstempel"], lesebestaetigung = sqlNachricht["Lesebestaetigung"])

def toNutzer(sqlNutzer: SQLNutzer) -> Nutzer:
    """
    Vor.: -
    Eff.: - 
    Erg.: Liefert die eingegebene SQLNachricht als Objekt der Klasse Nutzer wieder 
    """
    return Nutzer(UUID = UUID(sqlNutzer["ID"]), nutzername = sqlNutzer["Nutzername"], anzeigename = sqlNutzer["Anzeigename"])