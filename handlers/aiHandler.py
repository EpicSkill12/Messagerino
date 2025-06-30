from config.constants import AI_AGENT_NAME
from handlers.databaseHandler import database
from time import time as now

def sendAIMessage(message: str, recipient: str) -> None:
    database.createMessage(
        sender=AI_AGENT_NAME, 
        receiver=recipient,
        content=message,
        sendTime=now(),
        read=False
    )