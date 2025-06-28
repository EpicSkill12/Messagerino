# Initialisierung
# Loop: Anfrage empfangen
#       -> Database abfragen/ändern
#       -> Antwort senden
from custom_types.baseTypes import SQLUser
from handlers.databaseHandler import database
from helpers.encryptionHelper import getBaseModulusAndSecret, hashPW, decryptJson
from helpers.formattingHelper import makeResponse
from flask import Flask, request, jsonify
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
def getUser():
    username: Optional[str] = request.args.get("name")
    if not username:
        return makeResponse(obj={"error": "Parameter 'name' fehlt!"}, code=400)
    user: Optional[SQLUser] = database.findUser(username)
    if user:
        return jsonify({
            "username": user["Username"],
            "displayName": user["DisplayName"],
            "passwordHash": user["PasswordHash"],
            "creationDate": user["CreationDate"]
        }), 200
    else:
        return makeResponse(obj={"error": "Benutzer nicht gefunden!"}, code=404)

@server.route("/chats", methods = ["GET"])
def getChats(): #TODO: typ hinzufügen
    username: Optional[str] = request.args.get("name")
    if not username:
        return makeResponse(obj={"error": "Parameter 'name' fehlt!"}, code=400)
    return makeResponse(obj=database.findChatsByUser(username), code=200)

@server.route("/messages", methods = ["GET"])
def getMessagesByChat(): #TODO: s.o.
    username1: Optional[str] = request.args.get("name1")
    username2: Optional[str] = request.args.get("name2")
    if not username1:
        return makeResponse(obj={"error": "Parameter 'name1' fehlt!"}, code=400)
    if not username2:
        return makeResponse(obj={"error": "Parameter 'name2' fehlt!"}, code=400)
    return jsonify(database.findMessagesByChat(username1,username2)) 

@server.route("/suggestions", methods = ["GET"])
def getUserSuggestions(): #TODO: s.o.
    username: Optional[str] = request.args.get("name")
    if not username:
       return makeResponse(obj={"error": "Parameter 'name' fehlt!"}, code=400)
    return jsonify([row[0] for row in database.findSuggestionsByUser(username)]) #FIXME: Problem mit Flesk server bei der Namensübergabe (404 fehler)

@server.route("/session", methods = ["GET"])
def getSession():
    b, p, serverSecret = getBaseModulusAndSecret()
    id: str = str(uuid1())
    secrets[id] = (b, p, serverSecret)
    return makeResponse(obj={"base": b, "prime": p, "id": id}, code=200)

@server.route("/remainder", methods = ["GET"])
def getRemainder():
    remainderArg: Optional[str] = request.args.get("remainder")
    if not remainderArg:
        return makeResponse(obj={"error": "Parameter 'remainder' fehlt!"}, code=400)
    try:
        clientRemainder = int(remainderArg)
    except:
        return makeResponse(obj={"error": "Parameter 'remainder' ist keine Ganzzahl!"}, code=400)
    sessionID: Optional[str] = request.args.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"error": "Parameter 'sessionID' fehlt!"}, code=400)
    row: Optional[tuple[int, int, int]] = secrets.get(sessionID)
    if not row:
        return makeResponse(obj={"error": "sessionID konnte nicht gefunden werden"}, code=400)
    b, p, secret = row
    keys[sessionID] =pow(clientRemainder, secret, p)
    remainder = pow(b, secret, p)
    return jsonify({"remainder": remainder})

# === POST ===

@server.route("/user", methods = ["POST"])
def createUser(): #TODO: s.o.
    data = request.get_json()
    nutzername = data.get("nutzername")
    anzeigename = data.get("anzeigename")
    passwort = data.get("passwort")
    erstellungsdatum = data.get("erstellungsdatum", now())

    if not nutzername or not anzeigename or not passwort:
        return makeResponse(obj={"error": "Parameter 'nutzername', 'anzeigename' und 'passwort' erforderlich!"}, code=400)
    
    try:
        database.createUser(nutzername, anzeigename, passwort, erstellungsdatum)
        return makeResponse(obj={"message": "Benutzer erfolgreich erstellt!"}, code=201)
    except ValueError as error:
        return makeResponse(obj={"error": str(error)}, code=400)

@server.route("/user/update", methods =["POST"])
def updateUser(): #TODO: s.o.
    data = request.get_json()
    nutzername = data.get("nutzername")  
    neuerAnzeigename = data.get("anzeigename")
    neuesPasswort = data.get("passwort")

    if not nutzername:
        return makeResponse(obj={"error": "Parameter 'nutzername' erforderlich!"}, code=400)

    user: Optional[SQLUser] = database.findUser(nutzername)
    if not user:
        return makeResponse(obj={"error": "Benutzer nicht gefunden!"}, code=404)

    if neuerAnzeigename:
        user["DisplayName"] = neuerAnzeigename
    if neuesPasswort:
        user["PasswordHash"] = neuesPasswort

    try:
        database.updateUser(user) 
        return makeResponse(obj={"message": "Benutzer erfolgreich aktualisiert!"}, code=200)
    except Exception as e:
        return makeResponse(obj={"error": str(e)}, code=500)
    
@server.route("/message", methods =["POST"])
def sendMessage(): #TODO: s.o.
    data = request.get_json()
    sender = data.get("absender")
    empfaenger = data.get("empfaenger")
    inhalt = data.get("inhalt")
    zeitpunkt = data.get("zeitpunkt", now())
    read = data.get("lesebestaetigung", False)
    if not sender or not empfaenger or not inhalt:
        return makeResponse(obj={"error": "Parameter 'absender', 'empfaenger' und 'inhalt' erforderlich!"}, code=400)
    
    try: 
        database.createMessage(sender=sender, receiver=empfaenger, content=inhalt, sendTime=zeitpunkt, read=read)
        return makeResponse(obj={"message": "Nachricht erfolgreich gesendet!"}, code=201)
    except Exception as e:
        return makeResponse(obj={"error": str(e)}, code=500)

@server.route("/message/read", methods =["POST"])
def markMassageAsRead(): #TODO: s.o.
    data = request.get_json()
    id = data.get("uuid")

    if not id:
        return makeResponse(obj={"error": "Parameter 'uuid' erforderlich!"}, code=400)
    
    try:
        database.markeMessageAsRead(id)
        return makeResponse(obj={"message": "Nachricht als gelesen markiert."}, code=200)
    except Exception as e:
        return makeResponse(obj={"error": str(e)}, code=500)
    
@server.route("/login", methods = ["POST"])
def login(): #TODO s.o.
    sessionID = request.headers.get("sessionID")
    if not sessionID:
        return makeResponse(obj={"error": "Parameter 'sessionID fehlt"}, code=400)
    
    data = request.get_data()
    
    key = keys.get(sessionID)

    if not key:
        return makeResponse(obj={"error": "Ungültige SessionID!"}, code=400)
    try:
        decryptedData = decryptJson(cipherBlob=data, integer=key)
    except Exception as e:
        return makeResponse(obj={"error": "Konnte nicht entziffern!"}, code=500, encryptionKey=key)
    username = decryptedData.get("username")
    password = decryptedData.get("password")
    if not (username and password):
        return makeResponse(obj={"error": "'username' und 'password' müssen angegeben werden"}, code=400, encryptionKey=key)
    if not (isinstance(username, str) or isinstance(password, str)):
        return makeResponse(obj={"error": "'username' und 'password' müssen strings sein"}, code=400, encryptionKey=key)
    
    user = database.findUser(username)
    if not user:
        return makeResponse(obj={"error": "Benutzer existier nicht!"}, code=400, encryptionKey=key)
    
    if user["PasswordHash"] != hashPW(password):
        return makeResponse(obj={"error": "Falsches Passwort!"}, code=400, encryptionKey=key)
    
    try:
        return makeResponse(obj={"displayName": user["DisplayName"]}, code=200, encryptionKey=key)
    
    except Exception as e:
        return makeResponse(obj={"error": str(e)}, code=500, encryptionKey=key)
#========
#= MAIN
#========

if __name__ == "__main__":
    server.run(debug=True)