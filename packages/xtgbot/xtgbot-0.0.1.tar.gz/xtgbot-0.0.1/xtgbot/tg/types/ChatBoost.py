from .ChatBoostSource import ChatBoostSource
from ..base_type import base_type
from typing import Optional

@base_type
class ChatBoost:
    '''
    This object contains information about a chat boost.
    '''

    source: ChatBoostSource
    '''
    Source of the added boost
    '''

    expiration_date: int
    '''
    Point in time (Unix timestamp) when the boost will automatically expire, unless the booster's Telegram Premium subscription is prolonged
    '''

    add_date: int
    '''
    Point in time (Unix timestamp) when the chat was boosted
    '''

    boost_id: str
    '''
    Unique identifier of the boost
    '''

