from config.constants import AI_AGENT_NAME
from handlers.databaseHandler import database
from time import time as now
from custom_types.baseTypes import SQLMessage

locks: dict[str, bool] = {}

def sendAIMessage(message: str, recipient: str) -> None:
    database.createMessage(
        sender=AI_AGENT_NAME, 
        receiver=recipient,
        content=message,
        sendTime=now(),
        read=False
    )

def __getAIMessages(user: str) -> list[SQLMessage]:
    mine, yours = database.findMessagesByChat(AI_AGENT_NAME, user)
    return sorted(mine + yours, key=lambda m: m["SendTime"])

def isAIChatLocked(user: str) -> bool:
    global locks
    return locks.get(user, False)

def lockAIChat(user: str):
    global locks
    locks[user] = True

def __unlockAIChat(user: str):
    global locks
    locks[user] = False

def respondAIToUser(user: str) -> None:
    messages = __getAIMessages(user)
    lastMessage = messages[0]
    sendAIMessage(
        message=f'I hear you {lastMessage["Sender"]}: "{lastMessage["Content"]}"',
        recipient=user
    )

def respondAIToUsers() -> None:
    global locks
    for user, status in locks.items():
        if not status:
            continue
        respondAIToUser(user)
        __unlockAIChat(user)