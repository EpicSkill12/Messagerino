from config.constants import AI_AGENT_NAME, AI_SYSTEM_PROMPT, AI_SORRY_MESSAGE
from handlers.databaseHandler import database
from time import time as now
from custom_types.baseTypes import SQLMessage
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv("OPENAI_API_KEY")

locks: dict[str, bool] = {}

client = OpenAI(
  api_key=apiKey
)

def getCompletion(_messages: list[SQLMessage]) -> str:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": AI_SYSTEM_PROMPT}
    ]
    for message in _messages:
        role = "assistant" if message["Sender"] == AI_AGENT_NAME else "user"
        content = message["Content"]
        messages.append({"role": role, "content": content})
    
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
    )
    response = completion.choices[0].message.content
    return response if response else AI_SORRY_MESSAGE

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
    message = getCompletion(messages)
    sendAIMessage(
        message=message,
        recipient=user
    )

def respondAIToUsers() -> None:
    global locks
    for user, status in locks.items():
        if not status:
            continue
        respondAIToUser(user)
        __unlockAIChat(user)