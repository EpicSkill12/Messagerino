from string import punctuation

def validatePassword(validatee: str, validatee2: str) -> tuple[bool, str]:
    """
    Vor.: Zwei Passwort-Strings
    Eff.: -
    Erg.: Gibt True zurück wenn das Passwort Regeln erfüllt
    """
    if validatee != validatee2:
        return (False, "Passwort stimmt nicht überein!")
        
    if len(validatee) < 8 or len(validatee2) < 8:
        return (False, "Passwort muss mindestens 8 Zeichen lang sein!")
        
    if not any(c.isupper() for c in validatee):
        return (False, "Das Passwort muss mindestens einen Großbuchstaben enthalten!")
    
    if not any(c in punctuation for c in validatee):
        return (False, "Mindestens ein Sonderzeichen wie !@#%$ fehlt!")
    
    return (True, "")

def validateUser(validatee:str, validatee2:str) -> tuple[bool, str]:
    """
    Vor.: Zwei Strings für Nutzer- und Anzeigename
    Eff.: -
    Erg.: Gibt True zurück wenn die Namen gültig sind
    """
    if len(validatee) < 3 or len(validatee2) < 3:
        return (False, "Dein Nutzername und Anzeigename darf nicht kürzer als 3 Zeichen sein!")
    
    if len(validatee) > 10 or len(validatee2) > 10:  
        return (False, "Dein Nutzername und Anzeigename darf nicht länger als 10 Zeichen sein!")
    
    return (True, "")