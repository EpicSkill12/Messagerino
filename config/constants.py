from os import path
from typing import Literal

#* Sicherheit
UUID_MAX_TRIES: int = 3
BANNED_NAMES: list[str] = [
    "admin", 
    "owner", 
    "moderator", 
    "support", 
    "messagerino", 
    "chat", 
    "message", 
    "password", 
    "passwort", 
    "nachricht", 
    "besitzer", 
    "sicherheit",
    "agent"
]
SPECIAL_CHARACTERS: list[str] = [
    " ", "_", "-", ".", ",", "!", "?", "@", "#"
]
ALLOWED_CHARACTERS: list[str] = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
] + SPECIAL_CHARACTERS

#* Grafik
RESOLUTION: str = "1500x1000"
RESOLUTION_SECOND: str = "750x500"
MIN_SIZE_X: int = 1000
MIN_SIZE_Y: int = 750
MIN_SIZE_X2: int = 350
MIN_SIZE_Y2: int = 250
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
CHATS_WIDTH = 600
TOTAL_CHATS_WIDTH = SIDEBAR_WIDTH+CHATS_WIDTH
CHAT_HEIGHT = 80

MESSAGE_HEIGHT = 40
MESSAGE_WIDTH = 300
MESSAGE_MAX_LENGTH = 100


#* Ordner
ASSETS_FOLDER: str = "assets"
ICON_PATH = path.abspath(f"{ASSETS_FOLDER}/messagerino.ico")
LOGO_PATH = path.abspath(f"{ASSETS_FOLDER}/messagerino.png")
DB_PATH: str = "database.db"

#* Namen
NAME: str = "Messagerino"
AI_AGENT_NAME = "AI_AGENT"
AI_AGENT_DISPLAY_NAME = "Messagerino AI"
AI_AGENT_PASSWORD_HASH = "c5abbfd52385912b47516b1e3fd57f4cbb1798001da15867047bb8a43199145a"
FIRST_AI_MESSAGE = f"Hi! Ich bin {AI_AGENT_DISPLAY_NAME}, dein persönlicher KI-Assistent und freue mich auf unsere Konversation."

#* Netzwerk
IP: str = "84.157.207.57"
PORT: int = 5000
URL = f"{IP}:{PORT}"