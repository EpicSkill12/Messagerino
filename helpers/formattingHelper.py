import json
from datetime import datetime
from helpers.encryptionHelper import encryptJson
from typing import Literal, Any, Optional
from flask import Response

def formatTime(time: float):
    dateTime = datetime.fromtimestamp(time)
    return dateTime.strftime(r"%d.%m.%Y - %H:%M Uhr")

def getPossessive(name: str, language: Literal["en", "ger"] = "ger") -> str:
    versions = ("s", "'") if language == "ger" else ("'s", "'")
    if name[-1].lower() in ("s", "z", "ß", "x"):
        return name + versions[1]
    return name + versions[0]

def makeResponse(obj: Any, code: int, encryptionKey: Optional[int] = None) -> Response:
    if encryptionKey:
        return Response(response=encryptJson(obj=obj, integer=encryptionKey), status=code)
    else:
        return Response(json.dumps(obj), status=code)