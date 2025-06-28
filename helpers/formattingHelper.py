from datetime import datetime
from typing import Literal

def formatTime(time: float):
    dateTime = datetime.fromtimestamp(time)
    return dateTime.strftime(r"%d.%m.%Y - %H:%M Uhr")

def getPossessive(name: str, language: Literal["en", "ger"] = "ger") -> str:
    versions = ("s", "'") if language == "ger" else ("'s", "'")
    if name[-1].lower() in ("s", "z", "ß", "x"):
        return name + versions[1]
    return name + versions[0]