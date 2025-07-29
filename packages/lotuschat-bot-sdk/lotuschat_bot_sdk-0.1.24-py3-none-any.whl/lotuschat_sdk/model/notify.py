from enum import Enum
from typing import List

from pydantic import BaseModel

from src.lotuschat_sdk.model.query import User


class NotifyEvent(Enum):
    NEW_CHAT_MEMBERS = 1
    LEFT_CHAT_MEMBERS = 2


class BaseNotifyPayload(BaseModel): pass


class NewChatMemberPayload(BaseNotifyPayload):
    payload: List[User]


class LeftChatMemberPayload(BaseNotifyPayload):
    payload: User
