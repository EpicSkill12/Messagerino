# Initialisierung
# Loop: Anfrage empfangen
#       -> Database abfragen/ändern
#       -> Antwort senden
from handlers.databaseHandler import datenbank # type: ignore
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is your simple Flask server!"

if __name__ == "__main__":
    app.run(debug=True)