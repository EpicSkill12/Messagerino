# Initialisierung
# Loop: Anfrage empfangen
#       -> Database abfragen/ändern
#       -> Antwort senden
from custom_types.baseTypes import SQLUser
from handlers.databaseHandler import database
from flask import Flask, request, jsonify
from typing import Optional

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
        return jsonify(user), 200
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

if __name__ == "__main__":
    server.run(debug=True)