from sqlite3 import Connection, Cursor, connect
from uuid import UUID, uuid1
from custom_types.baseTypes import Result, SQLChat, SQLMessage, SQLUser, TupleMessage, TupleUser
from custom_types.httpTypes import HTTP
from helpers.encryptionHelper import hashPW
from helpers.conversionHelper import toSQLMessage, toSQLUser
from config.constants import DB_PATH, UUID_MAX_TRIES, AI_AGENT_NAME, AI_AGENT_DISPLAY_NAME, AI_AGENT_PASSWORD_HASH
from typing import Optional
from time import time as now

class Database():
    # === INITIALISIERUNG ===
    def __init__(self) -> None:
        self.__connection: Connection = connect(DB_PATH, check_same_thread=False)
        self.__cursor: Cursor = self.__connection.cursor()

        self.__cursor.execute("PRAGMA journal_mode=WAL")

        self.__connection.execute("PRAGMA busy_timeout=30000")  # 30 seconds
        self.__connection.commit()

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

        # KI-Assistent hinzufügen
        self.__cursor.execute(
            """
            INSERT INTO Nutzer (Nutzername, Anzeigename, PasswortHash, Erstellungsdatum)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(Nutzername) DO UPDATE SET
                Anzeigename = excluded.Anzeigename,
                PasswortHash = excluded.PasswortHash,
                Erstellungsdatum = excluded.Erstellungsdatum
            """,
            (AI_AGENT_NAME, AI_AGENT_DISPLAY_NAME, AI_AGENT_PASSWORD_HASH, now())
        )
        self.__connection.commit()
     
    # === Suche ===
    def findMessage(self, id: UUID) -> Optional[SQLMessage]:
        """
        Vor.: id ist eine UUID einer Nachricht aus der Datenbank
        Eff.: -
        Erg.: Die Nachricht mit der eingegebenen ID wird zurückgegeben
        """
        self.__cursor.execute(
            "SELECT * " \
            "FROM Nachrichten " \
            "WHERE UUID = ?",
            (str(id),)
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
            "SELECT * " \
            "FROM Nutzer " \
            "WHERE Nutzername = ? ",
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
        try:
            self.__cursor.execute(
                "UPDATE Nachrichten " \
                "SET Lesebestaetigung = 1 " \
                "WHERE Absender = ? " \
                "AND Empfaenger = ? ",
                (receiverName, senderName)
            )
            self.__connection.commit()
            self.__cursor.execute(
                "SELECT * " \
                "FROM Nachrichten " \
                "WHERE Absender = ? " \
                "AND Empfaenger = ? ",
                (senderName, receiverName)
                )
            result1: list[TupleMessage] = self.__cursor.fetchall()

            self.__cursor.execute(
                "SELECT * " \
                "FROM Nachrichten " \
                "WHERE Absender = ? " \
                "AND Empfaenger = ? ",
                (receiverName, senderName) 
            )
            result2: list[TupleMessage] = self.__cursor.fetchall()
            return ([toSQLMessage(element) for element in result1], [toSQLMessage(element) for element in result2])
        except Exception as e:
            self.__connection.rollback()
            print(f"Error in findMessagesByChat: {e}")
            return ([], [])
    
    def findSuggestionsByUser(self, username:str) -> list[tuple[str, str]]:
        """
        Vor.: username ist ein String eines existierenden Nutzers
        Eff.: -
        Erg.: Gibt eine Liste anderer Nutzer zurück
        """
        self.__cursor.execute(
        """
        SELECT Nutzername, Anzeigename 
        FROM Nutzer 
        WHERE Nutzername != ?
        """,
        (username,)
        )
        result: list[tuple[str, str]] = self.__cursor.fetchall()
        return result
    
    def findChatsByUser(self, username: str) -> list[SQLChat]:
        """
        Vor.: username ist ein String eines existierenden Nutzers
        Eff.: -
        Erg.: Gibt alle Chats des Nutzers zurück
        """
        self.__cursor.execute(
            """
            SELECT DISTINCT CASE 
                WHEN Absender = ? THEN Empfaenger
                ELSE Absender
            END AS ChatPartner
            FROM Nachrichten
            WHERE Absender = ? OR Empfaenger = ?
            """,
            (username,username, username)
        )
        results: list[str] = self.__cursor.fetchall()
        partners: list[str] = [row[0] for row in results]

        def getLastMessage(username: str, partnerName: str) -> SQLMessage:
            """
            Vor.: username und partnerName sind Strings
            Eff.: -
            Erg.: Gibt die zuletzt gesendete Nachricht zwischen beiden Nutzern zurück
            """
            self.__cursor.execute(
                """
                SELECT * FROM Nachrichten
                WHERE (Absender = ? AND Empfaenger = ?)
                    OR (Absender = ? AND Empfaenger = ?)
                ORDER BY Zeitstempel DESC
                LIMIT 1
                """,
                (username, partnerName, partnerName, username)
            )
            result: list[TupleMessage] = self.__cursor.fetchall()
            return (toSQLMessage(result[0]))
        
        finalResult:list[SQLChat] = []
        for partner in partners:
            finalResult.append({"Recipient": partner, "LastMessage": getLastMessage(username = username, partnerName = partner)})

        return finalResult

    # === Getter ===
    def getAllUser(self) -> list[SQLUser]:
        """
        Vor.: -
        Eff.: - 
        Erg.: Gibt alle Nutzer zurück
        """
        self.__cursor.execute(
            "SELECT * " \
            "FROM Nutzer"
        )
        result:list[TupleUser] = self.__cursor.fetchall()
        return [toSQLUser(element) for element in result]
    
    # === Setter ===
    def createUser(self, username:str, displayName: str, passwordHash: str, creationDate: float) -> Result:
        """
        Vor.: Alle Parameter sind gültige Strings bzw. float
        Eff.: Fügt einen neuen Nutzer in die Datenbank ein
        Erg.: Gibt das Resultat der Operation zurück
        """
        self.__cursor.execute(
            "SELECT 1 FROM Nutzer WHERE Nutzername = ?",
            (username,)
        )
        if self.__cursor.fetchone():
            return Result(False, f"Nutzername '{username}' existiert bereits.", HTTP.CONFLICT)

        self.__cursor.execute(
            "INSERT INTO Nutzer (Nutzername, Anzeigename, PasswortHash, Erstellungsdatum) " \
            "VALUES (?,?,?,?)",
            (username, displayName, passwordHash, creationDate)
        )
        self.__connection.commit()
        return Result(True, f"Nutzer '{username}' erfolgreich erstellt", HTTP.CREATED)

    def createMessage(self, sender: str, receiver:str, content: str, sendTime: float, read: bool = False) -> Result:
        """
        Vor.: sender und receiver existieren, content ist Text, sendTime eine Zahl
        Eff.: Fügt eine neue Nachricht in die Datenbank ein
        Erg.: Gibt das Resultat der Erstellung zurück
        """
        def createUUID() -> Optional[str]:
            """
            Vor.: -
            Eff.: Generiert eine freie UUID
            Erg.: Liefert eine eindeutige UUID oder None
            """
            for _ in range(UUID_MAX_TRIES):
                uuid = str(uuid1())

                self.__cursor.execute(
                    "SELECT 1 " \
                    "FROM Nachrichten " \
                    "WHERE UUID =  ?",
                    (uuid,)
                )
                if not self.__cursor.fetchone():
                    return uuid
            return None
        
        uuid: Optional[str] = createUUID()
        if not uuid:
            return Result(False, f"Konnte keine freie UUID nach {UUID_MAX_TRIES} Versuchen generieren", HTTP.INTERNAL_SERVER_ERROR)
        self.__cursor.execute(
            "INSERT INTO Nachrichten (UUID, Absender, Empfaenger, Inhalt, Zeitstempel, Lesebestaetigung) " \
            "VALUES (?,?,?,?,?,?)",
            (uuid, sender, receiver, content, sendTime, read)
        )
        self.__connection.commit()
        return Result(True, "Nachricht erfolgreich erstellt", HTTP.CREATED)

    def updateUser(self, user: SQLUser) -> Result:
        """
        Vor.: user ist ein gültiges SQLUser-Objekt
        Eff.: Aktualisiert dessen Eintrag in der Datenbank
        Erg.: Gibt das Resultat der Aktualisierung zurück
        """
        self.__cursor.execute(
            """
            UPDATE Nutzer 
            SET Anzeigename = ?, PasswortHash = ? 
            WHERE Nutzername = ?
            """,
            (user["DisplayName"], hashPW(user["PasswordHash"]), user["Username"])
        ) #!FIXME: hashPW?!
        self.__connection.commit()
        return Result(True, f"Nutzer '{user['Username']}' erfolgreich aktualisiert", HTTP.OK)
    
    def markMessageAsRead(self, uuid:str, user: str) -> Result:
        """
        Vor.: uuid gehört zu einer Nachricht, user ist der Empfänger
        Eff.: Setzt das Leseflag der Nachricht
        Erg.: Gibt das Resultat der Operation zurück
        """
        self.__cursor.execute(
            """
            SELECT Absender
            FROM Nachrichten 
            WHERE UUID = ?
            """,
            (uuid,)
        )
        if not (message := self.__cursor.fetchone()):
            return Result(False, f"Nachricht mit der ID '{uuid}' existiert nicht", HTTP.NOT_FOUND)
        if message[0] != user:
            return Result(False, f"Nutzer '{user}' kann diese Nachricht nicht lesen")
        self.__cursor.execute(
            """
            UPDATE Nachrichten 
            SET Lesebestaetigung = 1 
            WHERE UUID = ?
            """,
            (uuid,)
        )
        self.__connection.commit()
        return Result(True, f"Nachricht mit der ID '{uuid}' erfolgreich als gelesen markiert", HTTP.OK)

    def close(self) -> None:
        """
        Vor.: -
        Eff.: Schließt die Datenbankverbindung
        Erg.: -
        """
        try:
            self.__cursor.close()
            self.__connection.close()
        except Exception as e:
            print(f"Fehler beim Schließen der Datenbank: {e}")

    def __del__(self) -> None:
        """
        Vor.: -
        Eff.: Destruktor - schließt die Verbindung automatisch
        Erg.: -
        """
        self.close()

#========
#= CODE
#========

database = Database()