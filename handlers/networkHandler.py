from custom_types.baseTypes import Chat, User, Message
from uuid import uuid1
from config.constants import DEV_USER
from time import time as now

def getChats() -> list[Chat]:
    #! TODO: add network functionality
    user1 = User(uuid1(1), "user1", "First user",)
    user2 = User(uuid1(2), "user2", "The second user")
    message1 = Message(uuid1(11), senderName=user1, receiverName=DEV_USER, content="Hi, just wanted to ask you if you are able to even read this message, are you?", sendTime = 1750511332, read=False)
    message2 = Message(uuid1(11), senderName=DEV_USER, receiverName=user2, content="Thanks!", sendTime = now(), read=True)
    return [Chat(user1, lastMessage=message1), Chat(user2, message2)]