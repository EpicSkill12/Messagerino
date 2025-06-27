from custom_types.baseTypes import User
from time import time
from os import path
import hashlib

#* Graphics
RESOLUTION: str = "1000x1000"
FONT: tuple[str,int] = ("Arial", 12)
BIG_FONT: tuple[str,int] = ("Arial", 16)
TITLE_FONT: tuple[str, int, str] = ("Arial", 20, "bold")
MIN_SIZE_X: int = 500
MIN_SIZE_Y: int = 500

#* Paths
ASSETS_FOLDER: str = "assets"
ICON_PATH = path.abspath(f"{ASSETS_FOLDER}/messagerino.ico")
LOGO_PATH = path.abspath(f"{ASSETS_FOLDER}/messagerino.png")

sha256_hash = hashlib.sha256()
sha256_hash.update("ChrisTian!".encode('utf-8'))

#* Names
NAME:str = "Messagerino"
DEV_USER:User = User(username="debugy", displayName="Debugy", passwordHash=str(sha256_hash) , creationDate=time())

#* Paths
DB_PATH:str = "database.db"

#* Network
IP: str = "127.0.0.1"
PORT: int = 5000
URL = f"{IP}:{PORT}"