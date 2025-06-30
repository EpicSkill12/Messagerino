from helpers.encryptionHelper import decryptJson, makeKey
from helpers.encryptionHelper import encryptJson
from requests import get, post
from config.constants import URL
from custom_types.baseTypes import SQLChat, SQLMessage
from custom_types.httpTypes import HTTP
from typing import Optional

key: int = 0
sessionID: str = ""
myUsername: str = ""

def exchangeKey() -> tuple[int, str]:
    try:
        global key
        response = get(
            url=f"http://{URL}/session",
            timeout=5
        )
        sessionData = response.json()
        if response.status_code != HTTP.OK.value:
            return (False, sessionData.get("message"))
        b: int = sessionData.get("base")
        p: int = sessionData.get("prime")
        id: str = sessionData.get("id")
        secret: int = makeKey(p)
        response = get(
            url=f"http://{URL}/remainder",
            headers={
                "sessionID": id
            },
            params={
                "remainder": pow(b, secret, p)
            },
            timeout=5
        )
        remainderData = response.json()
        if response.status_code != HTTP.OK.value:
            return (False, remainderData.get("message"))
        remainder: int = remainderData.get("remainder")
        return (pow(remainder, secret, p), id)
    except Exception as e:
        return (False, str(e))

def trySignup(username: str, displayName: str, password: str) -> tuple[bool, str]:
    global key, sessionID, myUsername
    key, id = exchangeKey()
    if key == 0:
        return (False, id) # id ist die Fehlernachricht
    sessionID = id
    try:
        content = {
                "username": username,
                "displayName": displayName,
                "password": password
            }
        
        encryptedContent = encryptJson(obj=content, integer=key)
        
        response = post(
            url=f"http://{URL}/signup",
            headers={
                "sessionID": id
            },
            data = encryptedContent,
            timeout=5
        )
        try:
            data = response.json()
            success = response.status_code == HTTP.OK.value
            message = str(data.get("message"))
        except:
            try:
                data = decryptJson(response.content, key)
                success = response.status_code == HTTP.OK.value
                message = str(data.get("message"))
            except:
                success = False
                message = "Couldn't decrypt"
        
        myUsername = username
        return success, message
    except Exception as e:
        return False, f"Fehler: '{e}'"

def tryLogin(username: str, password: str) -> tuple[bool, str]:
    global key, sessionID, myUsername
    key, id = exchangeKey()
    if key == 0:
        return (False, id) # id ist die Fehlernachricht
    sessionID = id
    try:
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
        try:
            data = response.json()
            success = response.status_code == HTTP.OK.value
            message = data.get("displayName") if success else data.get("message")
        except:
            try:
                data = decryptJson(response.content, key)
                success = response.status_code == HTTP.OK.value
                message = str(data.get("displayName") if success else data.get("message"))
            except:
                success = False
                message = "Couldn't decrypt"
        
        myUsername = username
        return success, message
    except Exception as e:
        return False, f"Fehler: '{e}'"

def getOwnUsername() -> Optional[str]:
    response = get(
        url=f"http://{URL}/user/name",
        headers={
            "sessionID": sessionID
        },
        timeout=5
    )
    username = decryptJson(response.content, key).get("username")
    return username

def updateUser(displayName: str, password: str) -> tuple[bool, str]:
    content = {
                "nutzername": getOwnUsername(),
                "anzeigename": displayName,
                "passwort": password
            }
    encryptedContent = encryptJson(content, key)
    response = post(
            url=f"http://{URL}/user/update",
            headers={
                "sessionID": sessionID 
            },
            data = encryptedContent,
            timeout=5
        )
    if response.status_code != HTTP.OK.value:
        return (False, str(decryptJson(response.content, key).get("message")))
    
    return (True, str(decryptJson(response.content, key).get("message")))

def getChats() -> list[SQLChat]:
    content = encryptJson({"name": myUsername}, key)
    response = get(
        url=f"http://{URL}/chats",
        headers={
            "sessionID": sessionID
        },
        data=content,
        timeout=5
    )
    if response.status_code != HTTP.OK.value:
        message = decryptJson(response.content, key).get("message")
        print(str(message))
        return []
    sqlChats = decryptJson(response.content, key)
    if not (isinstance(sqlChats, list) and all(isinstance(chat, dict) for chat in sqlChats)):
        print(f"{str(sqlChats)} is no list of SQLChats")
        return []
    return sqlChats

def getUserSuggestions() -> list[str]:
    content = encryptJson({"name": myUsername}, key)
    response = get(
        url=f"http://{URL}/suggestions",
        headers={
            "sessionID": sessionID
        },
        data=content,
        timeout=5
    )
    if response.status_code != HTTP.OK.value:
        message = decryptJson(response.content, key).get("message")
        print(str(message))
        return []
    users = decryptJson(response.content, key)
    if not isinstance(users, list):
        print(f"{str(users)} is no list of Users!")
        return []
    return users

def getMessages(recipient: str) -> list[SQLMessage]:
    content = encryptJson({"name1": myUsername, "name2": recipient}, key)
    response = get(
        url=f"http://{URL}/messages",
        headers={
            "sessionID": sessionID
        },
        data=content,
        timeout=5
    )
    if response.status_code != HTTP.OK.value:
        message = decryptJson(response.content, key).get("message")
        print(str(message))
        return []
    myMessages, theirMessages = decryptJson(response.content, key)
    if not (isinstance(myMessages, list) and isinstance(theirMessages, list) and all(isinstance(message, dict) for message in myMessages) and all(isinstance(message, dict) for message in theirMessages)):
        print(f"{str(myMessages)} and {str(theirMessages)} are no lists of SQLMessages")
        return []
    messages: list[SQLMessage] = myMessages + theirMessages # type: ignore
    return sorted(messages, key=lambda m: m["SendTime"])

def sendMessage(inhalt: str, recipient: str) -> tuple[bool, str]:
    content = {
                "absender": myUsername,
                "empfaenger": recipient,
                "inhalt": inhalt
            }
    encryptedContent = encryptJson(content, key)
    response = post(
            url=f"http://{URL}/message",
            headers={
                "sessionID": sessionID 
            },
            data = encryptedContent,
            timeout=5
        )
    if response.status_code != HTTP.OK.value:
        return (False, str(decryptJson(response.content, key).get("message")))
    
    return (True, str(decryptJson(response.content, key).get("message")))