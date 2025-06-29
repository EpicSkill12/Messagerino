from os import path

#* Sicherheit
UUID_MAX_TRIES: int = 3

#* Grafik
RESOLUTION: str = "1500x1000"
FONT: tuple[str,int] = ("Arial", 12)
BIG_FONT: tuple[str,int] = ("Arial", 16)
TITLE_FONT: tuple[str, int, str] = ("Arial", 20, "bold")
MIN_SIZE_X: int = 1500
MIN_SIZE_Y: int = 1000
INTERFACE_COLOR: str = "#f0f0f0"

#* Ordner
ASSETS_FOLDER: str = "assets"
ICON_PATH = path.abspath(f"{ASSETS_FOLDER}/messagerino.ico")
LOGO_PATH = path.abspath(f"{ASSETS_FOLDER}/messagerino.png")
DB_PATH:str = "database.db"

#* Namen
NAME:str = "Messagerino"

#* Netzwerk
IP: str = "127.0.0.1"
PORT: int = 5000
URL = f"{IP}:{PORT}"