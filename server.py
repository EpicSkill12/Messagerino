# Initialisierung
# Loop: Anfrage empfangen
#       -> Database abfragen/ändern
#       -> Antwort senden
from custom_types.baseTypes import SQLUser
from custom_types.httpTypes import HTTP
from handlers.databaseHandler import database
from helpers.encryptionHelper import getBaseModulusAndSecret, hashPW, decryptJson
from helpers.formattingHelper import makeResponse
from flask import Response, Flask, request
from typing import Optional
from time import time as now
from uuid import uuid1

#========
#= CODE
#========

server = Flask(__name__)

# {UUID: (Basis, Modulus, Schlüssel)}
secrets: dict[str, tuple[int, int, int]] = {
}

keys: dict[str, int] = {
}

# === Basis ===

@server.route("/")
def home() -> str:
    return "Hello, this is Messagerino!"


# === GET ===

@server.route("/user", methods = ["GET"])
def getUser() -> Response: # TODO: passwords shall not be returned
    username: Optional[str] = request.args.get("name")
    if not username:
        return makeResponse(obj={"message": "Parameter 'name' fehlt!"}, code=HTTP.BAD_REQUEST)
    user: Optional[SQLUser] = database.findUser(username)
    if user:
        return makeResponse({
            "username": user["Username"],
            "displayName": user["DisplayName"],
            "passwordHash": user["PasswordHash"],
            "creationDate": user["CreationDate"]
        }, HTTP.OK)
    else:
        return makeResponse(obj={"message": "Benutzer nicht gefunden!"}, code=HTTP.NOT_FOUND)

@server.route("/chats", methods = ["GET"])
def getChats() -> Response:
    username: Optional[str] = request.args.get("name")
    if not username:
        return makeResponse(obj={"message": "Parameter 'name' fehlt!"}, code=HTTP.BAD_REQUEST)
    return makeResponse(obj=database.findChatsByUser(username), code=HTTP.OK)

@server.route("/messages", methods = ["GET"])
def getMessagesByChat() -> Response:
    username1: Optional[str] = request.args.get("name1")
    username2: Optional[str] = request.args.get("name2")
    if not username1:
        return makeResponse(obj={"message": "Parameter 'name1' fehlt!"}, code=HTTP.BAD_REQUEST)
    if not username2:
        return makeResponse(obj={"message": "Parameter 'name2' fehlt!"}, code=HTTP.BAD_REQUEST)
    return makeResponse(obj=database.findMessagesByChat(username1,username2), code=HTTP.OK) 

@server.route("/suggestions", methods = ["GET"])
def getUserSuggestions() -> Response:
    username: Optional[str] = request.args.get("name")
    if not username:
       return makeResponse(obj={"message": "Parameter 'name' fehlt!"}, code=HTTP.BAD_REQUEST)
    return makeResponse(obj=[row[0] for row in database.findSuggestionsByUser(username)], code=HTTP.OK)

@server.route("/session", methods = ["GET"])
def getSession() -> Response:
    b, p, serverSecret = getBaseModulusAndSecret()
    id: str = str(uuid1())
    secrets[id] = (b, p, serverSecret)
    return makeResponse(obj={"base": b, "prime": p, "id": id}, code=HTTP.OK)

@server.route("/remainder", methods = ["GET"])
def getRemainder() -> Response:
    remainderArg: Optional[str] = request.args.get("remainder")
    if not remainderArg:
        return makeResponse(obj={"message": "Parameter 'remainder' fehlt!"}, code=HTTP.BAD_REQUEST)
    try:
        clientRemainder = int(remainderArg)
    except:
        return makeResponse(obj={"message": "Parameter 'remainder' ist keine Ganzzahl!"}, code=HTTP.UNPROCESSABLE_ENTITY)
    sessionID: Optional[str] = request.args.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"message": "Parameter 'sessionID' fehlt!"}, code=HTTP.BAD_REQUEST)
    row: Optional[tuple[int, int, int]] = secrets.get(sessionID)
    if not row:
        return makeResponse(obj={"message": "sessionID konnte nicht gefunden werden"}, code=HTTP.NOT_FOUND)
    b, p, secret = row
    keys[sessionID] =pow(clientRemainder, secret, p)
    remainder = pow(b, secret, p)
    return makeResponse(obj={"remainder": remainder}, code=HTTP.OK)

# === POST ===

@server.route("/user", methods = ["POST"])
def createUser() -> Response:
    data = request.get_json()
    nutzername = data.get("nutzername")
    anzeigename = data.get("anzeigename")
    passwort = data.get("passwort")
    erstellungsdatum = data.get("erstellungsdatum", now())

    if not nutzername:
        return makeResponse(obj={"message": "Parameter 'nutzername' fehlt!"}, code=HTTP.BAD_REQUEST)
    if not anzeigename:
        return makeResponse(obj={"message": "Parameter 'anzeigename' fehlt!"}, code=HTTP.BAD_REQUEST)
    if not passwort:
        return makeResponse(obj={"message": "Parameter 'passwort' fehlt!"}, code=HTTP.BAD_REQUEST)
    
    result = database.createUser(nutzername, anzeigename, passwort, erstellungsdatum)
    return result.toResponse()

@server.route("/user/update", methods =["POST"])
def updateUser() -> Response:
    data = request.get_json()
    nutzername = data.get("nutzername")  
    neuerAnzeigename = data.get("anzeigename")
    neuesPasswort = data.get("passwort")

    if not nutzername:
        return makeResponse(obj={"message": "Parameter 'nutzername' fehlt!"}, code=HTTP.BAD_REQUEST)

    user: Optional[SQLUser] = database.findUser(nutzername)
    if not user:
        return makeResponse(obj={"message": "Benutzer nicht gefunden!"}, code=HTTP.NOT_FOUND)

    if neuerAnzeigename:
        user["DisplayName"] = neuerAnzeigename
    if neuesPasswort:
        user["PasswordHash"] = neuesPasswort

    result = database.updateUser(user) 
    return result.toResponse()
    
@server.route("/message", methods =["POST"])
def sendMessage() -> Response:
    data = request.get_json()
    sender = data.get("absender")
    empfaenger = data.get("empfaenger")
    inhalt = data.get("inhalt")
    zeitpunkt = data.get("zeitpunkt", now())
    read = data.get("lesebestaetigung", False)
    if not sender:
        return makeResponse(obj={"message": "Parameter 'absender' fehlt!"}, code=HTTP.BAD_REQUEST)
    if not empfaenger:
        return makeResponse(obj={"message": "Parameter 'empfaenger' fehlt!"}, code=HTTP.BAD_REQUEST)
    if not inhalt:
        return makeResponse(obj={"message": "Parameter 'inhalt' fehlt!"}, code=HTTP.BAD_REQUEST)
    
    result = database.createMessage(sender=sender, receiver=empfaenger, content=inhalt, sendTime=zeitpunkt, read=read)
    return result.toResponse()

@server.route("/message/read", methods =["POST"])
def markMassageAsRead() -> Response:
    data = request.get_json()
    id = data.get("uuid")

    if not id:
        return makeResponse(obj={"message": "Parameter 'uuid' fehlt!"}, code=HTTP.BAD_REQUEST)
    
    result = database.markMessageAsRead(id)
    return result.toResponse()
    
@server.route("/login", methods = ["POST"])
def login() -> Response:
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
    
    return makeResponse(obj={"displayName": user["DisplayName"]}, code=HTTP.OK, encryptionKey=key)

#========
#= MAIN
#========

if __name__ == "__main__":
    server.run(debug=True)