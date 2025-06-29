from os import path
from typing import Literal

#* Sicherheit
UUID_MAX_TRIES: int = 3

#* Grafik
RESOLUTION: str = "1500x1000"
FONT: tuple[str,int] = ("Arial", 12)
BIG_FONT: tuple[str,int] = ("Arial", 16)
TITLE_FONT: tuple[str, int, str] = ("Arial", 20, "bold")
MIN_SIZE_X: int = 1000
MIN_SIZE_Y: int = 750
INTERFACE_COLOR: str = "#f0f0f0"
MAX_SIZE_X: int = 1920
MAX_SIZE_Y: int = 1080
THEMES: dict[str,dict[Literal["background", "foreground", "buttonBG", "buttonFG", "highlight"], str]] = {
    "light": {
        "background": "#F4F4F4",
        "foreground": "#000000",
        "buttonBG": "#E0E0E0",
        "buttonFG": "#000000",
        "highlight": "#E74C3C"
    },
    "dark": {
        "background": "#2C3E50",
        "foreground": "#ECF0F1",
        "buttonBG": "#34495E",
        "buttonFG": "#ECF0F1",
        "highlight": "#E74C3C"
    }
}

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