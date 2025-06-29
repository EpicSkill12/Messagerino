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
THEMES: dict[str, dict[Literal["background", "foreground", "buttonBG", "buttonFG", "highlight"], str]] = {
    "light": {
        "background": "#FFFFFF",
        "foreground": "#1E1E1E",    
        "buttonBG": "#F3F3F3",       
        "buttonFG": "#1E1E1E",       
        "highlight": "#007ACC"       
    },
    "dark": {
        "background": "#1E1E1E",     
        "foreground": "#D4D4D4",     
        "buttonBG": "#2D2D30",       
        "buttonFG": "#FFFFFF",       
        "highlight": "#569CD6"      
    }
}
SIDEBAR_WIDTH = 60
CHATS_WIDTH = 270
TOTAL_CHATS_WIDTH = SIDEBAR_WIDTH+CHATS_WIDTH
CHAT_HEIGHT = 65


#* Ordner
ASSETS_FOLDER: str = "assets"
ICON_PATH = path.abspath(f"{ASSETS_FOLDER}/messagerino.ico")
LOGO_PATH = path.abspath(f"{ASSETS_FOLDER}/messagerino.png")
DB_PATH:str = "database.db"

#* Namen
NAME:str = "Messagerino"

#* Netzwerk
IP: str = "84.157.207.57"
PORT: int = 5000
URL = f"{IP}:{PORT}"