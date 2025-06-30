import json
from datetime import datetime
from helpers.encryptionHelper import encryptJson
from typing import Literal, Any, Optional
from flask import Response
from custom_types.httpTypes import HTTP

def formatTime(time: float):
    """
    Vor.: time ist ein Zeitstempel als float
    Eff.: -
    Erg.: Gibt den formatierten Zeitpunkt zurück
    """
    dateTime = datetime.fromtimestamp(time)
    return dateTime.strftime(r"%d.%m.%Y - %H:%M Uhr")

def getPossessive(name: str, language: Literal["en", "ger"] = "ger") -> str:
    """
    Vor.: name ist ein String
    Eff.: -
    Erg.: Gibt den besitzanzeigenden Namen zurück
    """
    versions = ("s", "'") if language == "ger" else ("'s", "'")
    if name[-1].lower() in ("s", "z", "ß", "x"):
        return name + versions[1]
    return name + versions[0]

def makeResponse(obj: Any, code: HTTP, encryptionKey: Optional[int] = None) -> Response:
    """
    Vor.: obj ist serialisierbar, code ist HTTP-Code
    Eff.: Erstellt eine verschlüsselte oder klare HTTP-Response
    Erg.: Flask Response-Objekt
    """
    if encryptionKey:
        return Response(response=encryptJson(obj=obj, integer=encryptionKey), status=code.value)
    else:
        return Response(json.dumps(obj), status=code.value)