from handlers.databaseHandler import database
from time import time as now
from hashlib import sha256

try:
    database.createUser(nutzername="Max", anzeigename="Maximus", passwortHash=sha256("789".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Anna", anzeigename="Anni", passwortHash=sha256("1011".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Tom", anzeigename="Tommy", passwortHash=sha256("1213".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Laura", anzeigename="Lauri", passwortHash=sha256("1415".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Julia", anzeigename="Jules", passwortHash=sha256("1617".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Peter", anzeigename="Peti", passwortHash=sha256("1819".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Sophie", anzeigename="Sofi", passwortHash=sha256("2021".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Simon", anzeigename="Simi", passwortHash=sha256("2223".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Mia", anzeigename="Mimi", passwortHash=sha256("2425".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Nico", anzeigename="Nick", passwortHash=sha256("2627".encode('utf-8')).hexdigest(), erstellungsdatum=now())
    database.createUser(nutzername="Felix", anzeigename="Feli", passwortHash=sha256("2829".encode('utf-8')).hexdigest(), erstellungsdatum=now())
except ValueError as fehler:
    print("Fehler:", fehler)