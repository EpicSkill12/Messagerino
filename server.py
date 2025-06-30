# Initialisierung
# Loop: Anfrage empfangen
#       -> Database abfragen/ändern
#       -> Antwort senden
import os
from custom_types.baseTypes import SQLUser
from custom_types.httpTypes import HTTP
from handlers.databaseHandler import database
from helpers.encryptionHelper import getBaseModulusAndSecret, hashPW, decryptJson
from helpers.formattingHelper import makeResponse
from helpers.gitHelper import getStatus, attemptPull
from flask import Response, Flask, request
from typing import Optional
from time import time as now
from uuid import uuid1

#========
#= CODE
#========

ROOT = os.path.dirname(os.path.abspath(__file__))

server = Flask(__name__)

# TODO: Sessions automatisch beenden
# {UUID: (Basis, Modulus, Schlüssel)}
secrets: dict[str, tuple[int, int, int]] = {
}

keys: dict[str, int] = {
}
sessionToUser: dict[str, str] = {
}

# === Basis ===

@server.route("/")
def home() -> str:
    """
    Vor.: -
    Eff.: Gibt einen Begrüßungstext zurück
    Erg.: Liefert einen String mit der Begrüßung
    """
    return "Hello, this is Messagerino!"

# === Wartung ===
@server.route('/gitStatus', methods=['GET'])
def debug() -> Response:
    """
    Vor.: -
    Eff.: Liest den Git-Status des Server-Verzeichnisses aus
    Erg.: Gibt eine HTTP-Response mit dem Status zurück
    """
    success, message = getStatus(ROOT)
    if success:
        return makeResponse({"message": message.splitlines()}, HTTP.OK)
    else:
        return makeResponse({"message": message.splitlines()}, HTTP.INTERNAL_SERVER_ERROR)

#*POST
@server.route("/update", methods=["POST"])
def update() -> Response:
    """
    Vor.: -
    Eff.: Führt einen Git-Pull im Server-Verzeichnis aus
    Erg.: Gibt eine HTTP-Response mit dem Ergebnis zurück
    """
    success, message = attemptPull(ROOT)
    if success:
        return makeResponse({"message": message.splitlines()}, HTTP.OK)
    else:
        return makeResponse({"message": message.splitlines()}, HTTP.INTERNAL_SERVER_ERROR)

# === GET ===

@server.route("/user/name", methods=["GET"])
def getUsername() -> Response:
    """
    Vor.: Header 'sessionID' muss gesetzt sein
    Eff.: Kein Effekt auf Serverdaten
    Erg.: Liefert den Benutzernamen der aktiven Sitzung
    """
    # Autorisierung
    sessionID: Optional[str] = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Header 'sessionID' fehlt"}, code=HTTP.UNAUTHORIZED)
    key = keys.get(sessionID)
    if not key:
        return makeResponse(obj={"message": "Ungültige sessionID"}, code=HTTP.NOT_FOUND)
    username = sessionToUser[sessionID]
    return makeResponse(obj={"username": username}, code=HTTP.OK, encryptionKey=key)

@server.route("/user", methods = ["GET"])
def getUser() -> Response:
    """
    Vor.: Query-Parameter 'name' muss ein existierender Nutzername sein
    Eff.: Keine Veränderung in der Datenbank
    Erg.: Gibt Nutzerdaten oder eine Fehlermeldung zurück
    """
    username: Optional[str] = request.args.get("name")
    if not username:
        return makeResponse(obj={"message": "Parameter 'name' fehlt!"}, code=HTTP.BAD_REQUEST)
    user: Optional[SQLUser] = database.findUser(username)
    if user:
        return makeResponse({
            "username": user["Username"],
            "displayName": user["DisplayName"],
            "passwordHash": "Passwörter werden bei Messagerino sicher verwahrt",
            "creationDate": user["CreationDate"]
        }, HTTP.OK)
    else:
        return makeResponse(obj={"message": "Benutzer nicht gefunden!"}, code=HTTP.NOT_FOUND)

@server.route("/chats", methods = ["GET"])
def getChats() -> Response:
    """
    Vor.: Header 'sessionID' und verschlüsselte Daten mit 'name' müssen vorhanden sein
    Eff.: Keine Veränderung an Serverdaten
    Erg.: Gibt eine Liste der Chats des Nutzers zurück
    """
    # Autorisierung
    sessionID: Optional[str] = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Header 'sessionID' fehlt"}, code=HTTP.UNAUTHORIZED)
    key = keys.get(sessionID)
    if not key:
        return makeResponse(obj={"message": "Ungültige sessionID"}, code=HTTP.NOT_FOUND)
    args = decryptJson(request.data, key)
    username: Optional[str] = args.get("name")
    if not username:
        return makeResponse(obj={"message": "Parameter 'name' fehlt!"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not username == sessionToUser[sessionID]:
        return makeResponse(obj={"message": "Falscher Nutzer"}, code=HTTP.FORBIDDEN)
    
    return makeResponse(obj=database.findChatsByUser(username), code=HTTP.OK, encryptionKey=key)

@server.route("/messages", methods = ["GET"])
def getMessagesByChat() -> Response:
    """
    Vor.: Header 'sessionID' sowie verschlüsselte Daten mit 'name1' und 'name2'
    Eff.: Markiert Nachrichten des Chatpartners als gelesen
    Erg.: Gibt die Nachrichten des Chats zurück
    """
    # Autorisierung
    sessionID: Optional[str] = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Header 'sessionID' fehlt"}, code=HTTP.UNAUTHORIZED)
    key = keys.get(sessionID)
    if not key:
        return makeResponse(obj={"message": "Ungültige sessionID"}, code=HTTP.NOT_FOUND)
    
    args = decryptJson(request.data, key)
    
    username1: Optional[str] = args.get("name1")
    username2: Optional[str] = args.get("name2")
    
    if not username1:
        return makeResponse(obj={"message": "Parameter 'name1' fehlt!"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not username2:
        return makeResponse(obj={"message": "Parameter 'name2' fehlt!"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    
    if username1 != sessionToUser[sessionID]:
        return makeResponse(obj={"message": "Dieser Nutzer hat keinen Zugriff auf diesen Chat"}, code=HTTP.FORBIDDEN, encryptionKey=key)
    
    return makeResponse(obj=database.findMessagesByChat(username1,username2), code=HTTP.OK, encryptionKey=key) 

@server.route("/suggestions", methods = ["GET"])
def getUserSuggestions() -> Response:
    """
    Vor.: Header 'sessionID' und verschlüsselte Daten mit 'name' vorhanden
    Eff.: -
    Erg.: Gibt mögliche Chatpartner des Nutzers zurück
    """
    # Autorisierung
    sessionID: Optional[str] = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Header 'sessionID' fehlt"}, code=HTTP.UNAUTHORIZED)
    key = keys.get(sessionID)
    if not key:
        return makeResponse(obj={"message": "Ungültige sessionID"}, code=HTTP.NOT_FOUND)
    args = decryptJson(request.data, key)
    username: Optional[str] = args.get("name")
    if not username == sessionToUser[sessionID]:
        return makeResponse(obj={"message": "Falscher Nutzer"}, code=HTTP.FORBIDDEN)
    if not username:
       return makeResponse(obj={"message": "Parameter 'name' fehlt!"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    return makeResponse(obj=database.findSuggestionsByUser(username), code=HTTP.OK, encryptionKey=key)

@server.route("/session", methods = ["GET"])
def getSession() -> Response:
    """
    Vor.: -
    Eff.: Erstellt eine neue Session mit Schlüssel und speichert sie
    Erg.: Gibt Basis, Primzahl und Session-ID zurück
    """
    b, p, serverSecret = getBaseModulusAndSecret()
    id: str = str(uuid1())
    secrets[id] = (b, p, serverSecret)
    return makeResponse(obj={"base": b, "prime": p, "id": id}, code=HTTP.OK)

@server.route("/remainder", methods = ["GET"])
def getRemainder() -> Response:
    """
    Vor.: Header 'sessionID' und Parameter 'remainder' als Ganzzahl vorhanden
    Eff.: Speichert den geteilten Schlüssel der Sitzung
    Erg.: Liefert den eigenen Restwert zum Schlüsselabgleich
    """
    remainderArg: Optional[str] = request.args.get("remainder")
    if not remainderArg:
        return makeResponse(obj={"message": "Parameter 'remainder' fehlt!"}, code=HTTP.BAD_REQUEST)
    try:
        clientRemainder = int(remainderArg)
    except:
        return makeResponse(obj={"message": "Parameter 'remainder' ist keine Ganzzahl!"}, code=HTTP.UNPROCESSABLE_ENTITY)
    sessionID: Optional[str] = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Header 'sessionID' fehlt!"}, code=HTTP.BAD_REQUEST)
    row: Optional[tuple[int, int, int]] = secrets.get(sessionID)
    if not row:
        return makeResponse(obj={"message": "sessionID konnte nicht gefunden werden"}, code=HTTP.NOT_FOUND)
    b, p, secret = row
    keys[sessionID] =pow(clientRemainder, secret, p)
    remainder = pow(b, secret, p)
    return makeResponse(obj={"remainder": remainder}, code=HTTP.OK)

# === POST ===

@server.route("/user/update", methods =["POST"])
def updateUser() -> Response:
    """
    Vor.: Gültige 'sessionID' und verschlüsselte Nutzerdaten
    Eff.: Aktualisiert Nutzerdaten in der Datenbank
    Erg.: Gibt eine HTTP-Response über den Erfolg zurück
    """
    # Autorisierung
    sessionID: Optional[str] = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Header 'sessionID' fehlt"}, code=HTTP.UNAUTHORIZED)
    key = keys.get(sessionID)
    if not key:
        return makeResponse(obj={"message": "Ungültige sessionID"}, code=HTTP.NOT_FOUND, encryptionKey=key)
    
    data = decryptJson(request.data, key)
    username = data.get("nutzername")  
    newDisplayName = data.get("anzeigename")
    newPassword = data.get("passwort")

    if not username:
        return makeResponse(obj={"message": "Parameter 'nutzername' fehlt!"}, code=HTTP.BAD_REQUEST, encryptionKey=key)

    if not username == sessionToUser[sessionID]:
        return makeResponse(obj={"message": f"{sessionToUser[sessionID]} darf nicht das Profil von {username} bearbeiten"}, code=HTTP.FORBIDDEN, encryptionKey=key)
    
    user: Optional[SQLUser] = database.findUser(username)
    if not user:
        return makeResponse(obj={"message": "Benutzer nicht gefunden!"}, code=HTTP.NOT_FOUND, encryptionKey=key)

    if newDisplayName:
        user["DisplayName"] = newDisplayName
    if newPassword:
        user["PasswordHash"] = newPassword

    result = database.updateUser(user) 
    return result.toResponse(encryptionKey=key)
    
@server.route("/message", methods =["POST"])
def sendMessage() -> Response:
    """
    Vor.: Header 'sessionID' und verschlüsselte Nachrichtendaten vorhanden
    Eff.: Legt eine neue Nachricht in der Datenbank an
    Erg.: Gibt eine HTTP-Response mit dem Ergebnis zurück
    """
    # Autorisierung
    sessionID: Optional[str] = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Header 'sessionID' fehlt"}, code=HTTP.UNAUTHORIZED)
    key = keys.get(sessionID)
    if not key:
        return makeResponse(obj={"message": "Ungültige sessionID"}, code=HTTP.NOT_FOUND)
    
    data = decryptJson(request.data, key)
    sender = data.get("absender")
    receiver = data.get("empfaenger")
    inhalt = data.get("inhalt")
    sendTime = data.get("zeitpunkt", now())
    read = data.get("lesebestaetigung", 0)
    if not sender:
        return makeResponse(obj={"message": "Parameter 'absender' fehlt!"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not sender == sessionToUser[sessionID]:
        return makeResponse(obj={"message": f"'{sessionToUser[sessionID]}' darf nicht als '{sender}' senden"}, code=HTTP.FORBIDDEN, encryptionKey=key)
    if not receiver:
        return makeResponse(obj={"message": "Parameter 'empfaenger' fehlt!"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not inhalt:
        return makeResponse(obj={"message": "Parameter 'inhalt' fehlt!"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not isinstance(sendTime, float):
        return makeResponse(obj={"message": "Parameter 'zeitpunkt' muss eine Dezimalzahl sein!"}, code=HTTP.UNPROCESSABLE_ENTITY, encryptionKey=key)
    
    
    
    result = database.createMessage(sender=sender, receiver=receiver, content=inhalt, sendTime=sendTime, read=read)
    return result.toResponse(encryptionKey=key)

@server.route("/message/read", methods =["POST"])
def markMassageAsRead() -> Response:
    """
    Vor.: Header 'sessionID' und JSON mit 'uuid' vorhanden
    Eff.: Markiert eine Nachricht als gelesen
    Erg.: Gibt eine HTTP-Response über den Erfolg zurück
    """
    # Autorisierung
    sessionID: Optional[str] = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Header 'sessionID' fehlt"}, code=HTTP.UNAUTHORIZED)
    key = keys.get(sessionID)
    if not key:
        return makeResponse(obj={"message": "Ungültige sessionID"}, code=HTTP.NOT_FOUND)
    
    data = request.get_json()
    id = data.get("uuid")

    if not id:
        return makeResponse(obj={"message": "Parameter 'uuid' fehlt!"}, code=HTTP.BAD_REQUEST)
    
    result = database.markMessageAsRead(id, sessionToUser[sessionID])
    return result.toResponse()

@server.route("/signup", methods = ["POST"])
def signup() -> Response:
    """
    Vor.: Header 'sessionID' und verschlüsselte Registrierungsdaten
    Eff.: Legt einen neuen Nutzer in der Datenbank an
    Erg.: Gibt eine Bestätigung oder Fehlermeldung zurück
    """
    sessionID = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Parameter 'sessionID fehlt"}, code=HTTP.BAD_REQUEST)
    
    data = request.get_data()
    
    key = keys.get(sessionID)

    if not key:
        return makeResponse(obj={"message": "Ungültige SessionID!"}, code=HTTP.NOT_FOUND)
    try:
        decryptedData = decryptJson(cipherBlob=data, integer=key)
    except Exception:
        return makeResponse(obj={"message": "Konnte nicht entschlüsseln!"}, code=HTTP.UNAUTHORIZED, encryptionKey=key)
    username = decryptedData.get("username")
    displayName = decryptedData.get("displayName")
    password = decryptedData.get("password")
    if not username:
        return makeResponse(obj={"message": "'username' fehlt"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not displayName:
        return makeResponse(obj={"message": "'displayName' fehlt"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not password:
        return makeResponse(obj={"message": "'password' fehlt"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not isinstance(username, str):
        return makeResponse(obj={"message": "'username' muss ein string sein"}, code=HTTP.UNPROCESSABLE_ENTITY, encryptionKey=key)
    if not isinstance(displayName, str):
        return makeResponse(obj={"message": "'displayName' muss ein string sein"}, code=HTTP.UNPROCESSABLE_ENTITY, encryptionKey=key)
    if not isinstance(password, str):
        return makeResponse(obj={"message": "'password' muss ein string sein"}, code=HTTP.UNPROCESSABLE_ENTITY, encryptionKey=key)
    
    user = database.findUser(username)
    if user:
        return makeResponse(obj={"message": "Benutzer existiert bereits!"}, code=HTTP.CONFLICT, encryptionKey=key)
    
    database.createUser(username, displayName, hashPW(password), now())
    
    sessionToUser[sessionID] = username
    return makeResponse(obj={"message": f"Nutzer '{username}' erfolgreich erstellt"}, code=HTTP.OK, encryptionKey=key)

@server.route("/login", methods = ["POST"])
def login() -> Response:
    """
    Vor.: Header 'sessionID' und verschlüsselte Logindaten vorhanden
    Eff.: Speichert Nutzername in aktueller Sitzung
    Erg.: Liefert den Anzeigenamen oder eine Fehlermeldung
    """
    sessionID = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Parameter 'sessionID fehlt"}, code=HTTP.BAD_REQUEST)
    
    data = request.get_data()
    
    key = keys.get(sessionID)

    if not key:
        return makeResponse(obj={"message": "Ungültige SessionID!"}, code=HTTP.NOT_FOUND)
    try:
        decryptedData = decryptJson(cipherBlob=data, integer=key)
    except Exception:
        return makeResponse(obj={"message": "Konnte nicht entschlüsseln!"}, code=HTTP.UNAUTHORIZED, encryptionKey=key)
    username = decryptedData.get("username")
    password = decryptedData.get("password")
    if not username:
        return makeResponse(obj={"message": "'username' fehlt"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not password:
        return makeResponse(obj={"message": "'password' fehlt"}, code=HTTP.BAD_REQUEST, encryptionKey=key)
    if not isinstance(username, str):
        return makeResponse(obj={"message": "'username' muss ein string sein"}, code=HTTP.UNPROCESSABLE_ENTITY, encryptionKey=key)
    if not isinstance(password, str):
        return makeResponse(obj={"message": "'password' muss ein string sein"}, code=HTTP.UNPROCESSABLE_ENTITY, encryptionKey=key)
    
    user = database.findUser(username)
    if not user:
        return makeResponse(obj={"message": "Benutzer existiert nicht!"}, code=HTTP.NOT_FOUND, encryptionKey=key)
    
    if user["PasswordHash"] != hashPW(password):
        return makeResponse(obj={"message": "Falsches Passwort!"}, code=HTTP.UNAUTHORIZED, encryptionKey=key)
    
    sessionToUser[sessionID] = username
    return makeResponse(obj={"displayName": user["DisplayName"]}, code=HTTP.OK, encryptionKey=key)


#========
#= MAIN
#========

if __name__ == "__main__":
    server.run(host= "0.0.0.0", debug=True)