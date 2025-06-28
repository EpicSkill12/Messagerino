# Initialisierung
# Loop: Anfrage empfangen
#       -> Database abfragen/ändern
#       -> Antwort senden
from custom_types.baseTypes import SQLUser
from handlers.databaseHandler import database
from handlers.encryptionHandler import getBaseModulusAndSecret
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
        return jsonify({"error": "Parameter 'name' fehlt!"}), 400
    user: Optional[SQLUser] = database.findUser(username)
    if user:
        return jsonify({
            "username": user["Username"],
            "displayName": user["DisplayName"],
            "passwordHash": user["PasswordHash"],
            "creationDate": user["CreationDate"]
        }), 200
    else:
        return jsonify({"error": "Benutzer nicht gefunden!"}), 404

@server.route("/chats", methods = ["GET"])
def getChats(): #TODO: typ hinzufügen
    username: Optional[str] = request.args.get("name")
    if not username:
        return jsonify({"error": "Parameter 'name' fehlt!"}), 400
    return jsonify(database.findChatsByUser(username)), 200

@server.route("/messages", methods = ["GET"])
def getMessagesByChat(): #TODO: s.o.
    username1: Optional[str] = request.args.get("name1")
    username2: Optional[str] = request.args.get("name2")
    if not username1:
        return jsonify({"error": "Parameter 'name1' fehlt!"}), 400
    if not username2:
        return jsonify({"error": "Parameter 'name2' fehlt!"}), 400
    return jsonify(database.findMessagesByChat(username1,username2)) 

@server.route("/suggestions", methods = ["GET"])
def getUserSuggestions(): #TODO: s.o.
    username: Optional[str] = request.args.get("name")
    if not username:
       return jsonify({"error": "Parameter 'name' fehlt!"}), 400
    return jsonify([row[0] for row in database.findSuggestionsByUser(username)]) #FIXME: Problem mit Flesk server bei der Namensübergabe (404 fehler)

@server.route("/session", methods = ["GET"])
def getSession():
    b, p, serverSecret = getBaseModulusAndSecret()
    id: str = str(uuid1())
    secrets[id] = (b, p, serverSecret)
    return jsonify({"base": b, "prime": p, "id": id}), 200

@server.route("/remainder", methods = ["GET"])
def getRemainder():
    remainderArg: Optional[str] = request.args.get("remainder")
    if not remainderArg:
        return jsonify({"error": "Parameter 'remainder' fehlt!"}), 400
    try:
        clientRemainder = int(remainderArg)
    except:
        return jsonify({"error": "Parameter 'remainder' ist keine Ganzzahl!"}), 400
    
    sessionID: Optional[str] = request.args.get("sessionID")
    if not sessionID:
        return jsonify({"error": "Parameter 'sessionID' fehlt!"}), 400
    row: Optional[tuple[int, int, int]] = secrets.get(sessionID)
    if not row:
        return jsonify({"error": "sessionID konnte nicht gefunden werden"}), 400
    
    b, p, secret = row
    keys[sessionID] = clientRemainder**secret % p
    
    remainder = b**secret % p
    
    return remainder

# === POST ===

@server.route("/user", methods = ["POST"])
def createUser(): #TODO: s.o.
    data = request.get_json()
    nutzername = data.get("nutzername")
    anzeigename = data.get("anzeigename")
    passwort = data.get("passwort")
    erstellungsdatum = data.get("erstellungsdatum", now())

    if not nutzername or not anzeigename or not passwort:
        return jsonify({"error": "Parameter 'nutzername', 'anzeigename' und 'passwort' erforderlich!"}), 400
    
    try:
        database.createUser(nutzername, anzeigename, passwort, erstellungsdatum)
        return jsonify({"message": "Benutzer erfolgreich erstellt!"}), 201
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

@server.route("/user/update", methods =["POST"])
def updateUser(): #TODO: s.o.
    data = request.get_json()
    nutzername = data.get("nutzername")  
    neuerAnzeigename = data.get("anzeigename")
    neuesPasswort = data.get("passwort")

    if not nutzername:
        return jsonify({"error": "Parameter 'nutzername' erforderlich!"}), 400

    user: Optional[SQLUser] = database.findUser(nutzername)
    if not user:
        return jsonify({"error": "Benutzer nicht gefunden!"}), 404

    if neuerAnzeigename:
        user["DisplayName"] = neuerAnzeigename
    if neuesPasswort:
        user["PasswordHash"] = neuesPasswort

    try:
        database.updateUser(user) 
        return jsonify({"message": "Benutzer erfolgreich aktualisiert!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@server.route("/message", methods =["POST"])
def sendMessage(): #TODO: s.o.
    data = request.get_json()
    sender = data.get("absender")
    empfaenger = data.get("empfaenger")
    inhalt = data.get("inhalt")
    zeitpunkt = data.get("zeitpunkt", now())
    read = data.get("lesebestaetigung", False)
    if not sender or not empfaenger or not inhalt:
        return jsonify({"error": "Parameter 'absender', 'empfaenger' und 'inhalt' erforderlich!"}), 400
    
    try: 
        database.createMessage(sender=sender, receiver=empfaenger, content=inhalt, sendTime=zeitpunkt, read=read)
        return jsonify({"message": "Nachricht erfolgreich gesendet!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
#========
#= MAIN
#========

if __name__ == "__main__":
    server.run(debug=True)