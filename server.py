# Initialisierung
# Loop: Anfrage empfangen
#       -> Database abfragen/ändern
#       -> Antwort senden
from custom_types.baseTypes import SQLUser
from handlers.databaseHandler import database
from flask import Flask, request, jsonify
from typing import Optional
from time import time as now

#========
#= CODE
#========

server = Flask(__name__)


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

@server.route("/message/read", methods =["POST"])
def markMassageAsRead(): #TODO: s.o.
    data = request.get_json()
    id = data.get("uuid")

    if not id:
        return jsonify({"error": "Parameter 'uuid' erforderlich!"}), 400
    
    try:
        database.markeMessageAsRead(id)
        return jsonify({"message": "Nachricht als gelesen markiert."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#========
#= MAIN
#========

if __name__ == "__main__":
    server.run(debug=True)