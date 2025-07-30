from .Chat import Chat
from .ChatBoostSource import ChatBoostSource
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class ChatBoostRemoved:
    '''
    This object represents a boost removed from a chat.
    '''

    source: ChatBoostSource
    '''
    Source of the removed boost
    '''

    remove_date: int
    '''
    Point in time (Unix timestamp) when the boost was removed
    '''

    boost_id: str
    '''
    Unique identifier of the boost
    '''

    chat: Chat
    '''
    Chat which was boosted
    '''

