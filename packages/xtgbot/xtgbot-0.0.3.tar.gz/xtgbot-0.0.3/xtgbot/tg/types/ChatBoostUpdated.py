from .Chat import Chat
from .ChatBoost import ChatBoost
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class ChatBoostUpdated:
    '''
    This object represents a boost added to a chat or changed.
    '''

    boost: ChatBoost
    '''
    Information about the chat boost
    '''

    chat: Chat
    '''
    Chat which was boosted
    '''

