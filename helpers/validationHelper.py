from handlers.interfaceHandler import benutzeroberflaeche
from string import punctuation

def validatePassword(validatee: str, validatee2: str) -> tuple[bool, str]:
    if validatee != validatee2:
            return (False, "Passwort stimmt nicht überein!")
        
    if len(validatee) < 8 or len(validatee2) < 8:
            benutzeroberflaeche.__fehlermeldung.config(text = "Passwort muss mindestens 8 Zeichen lang sein!")
            return
        
    if not any(c.isupper() for c in validatee):
            benutzeroberflaeche.__fehlermeldung.config(text = "Das Passwort muss mindestens einen Großbuchstaben enthalten!")
            return
        
    if not any(c in punctuation for c in validatee):
            benutzeroberflaeche.__fehlermeldung.config(text = "Mindestens ein Sonderzeichen wie !@#%$ fehlt!")
            return