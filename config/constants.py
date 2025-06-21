from custom_types.baseTypes import User
from uuid import uuid1
#* Graphics
RESOLUTION: str = "1000x1000"
FONT: tuple[str,int] = ("Arial", 12)
BIG_FONT: tuple[str,int] = ("Arial", 16)
TITLE_FONT: tuple[str, int, str] = ("Arial", 20, "bold")
MIN_SIZE_X: int = 500
MIN_SIZE_Y: int = 500

#* Names
NAME:str = "Messagerino"
DEV_USER:User = User(UUID=uuid1(0), username="debugy", displayName="Debugy")

#* Paths
DB_PATH:str = "database.db"