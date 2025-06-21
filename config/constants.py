from custom_types.baseTypes import User
#* Graphics
RESOLUTION: str = "1000x1000"
FONT: tuple[str,int] = ("Arial", 12)
BIG_FONT: tuple[str,int] = ("Arial", 16)
TITLE_FONT: tuple[str, int, str] = ("Arial", 20, "bold")
MIN_SIZE_X: int = 500
MIN_SIZE_Y: int = 500

#* Names
NAME = "Messagerino"
DEV_USER = User(UUID="278f98b8-4ea0-11f0-bfaa-000000000000", username="debugy", displayName="Debugy")

#* Paths
DB_PATH = "datenbank.db"