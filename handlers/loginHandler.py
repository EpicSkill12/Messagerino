from helpers.encryptionHelper import decryptJson, makeKey
from helpers.encryptionHelper import encryptJson
from requests import get, post
from config.constants import URL

key: int = 0

def tryLogin(username: str, password: str) -> tuple[bool, str]:
    global key
    try:
        response = get(
            url=f"http://{URL}/session",
            timeout=5
        )

        sessionData = response.json()
        b: int = sessionData.get("base")
        p: int = sessionData.get("prime")
        id: str = sessionData.get("id")

        secret: int = makeKey(p)
        response = get(
            url=f"http://{URL}/remainder",
            params={
                "remainder": pow(b, secret, p), 
                "sessionID": id
            },
            timeout=5
        )
        remainderData = response.json()
        remainder: int = remainderData.get("remainder")
        key = pow(remainder, secret, p)
        
        content = {
                "username": username,
                "password": password
            }
        
        encryptedContent = encryptJson(obj=content, integer=key)
        
        response = post(
            url=f"http://{URL}/login",
            headers={
                "sessionID": id
            },
            data = encryptedContent,
            timeout=5
        )
        try: # ? TODO: more elegant solution, connectionHelper?
            data = response.json()
            success = response.status_code == 200
            message = data.get("displayName") if success else data.get("error")
        except:
            try:
                data = decryptJson(response.content, key)
                success = response.status_code == 200
                message = str(data.get("displayName") if success else data.get("error"))
            except:
                success = False
                message = "Couldn't decrypt"
        
        
        return success, message
    except Exception as e:
        return False, f"Fehler: '{e}'"
    
    # get successStatus
    
