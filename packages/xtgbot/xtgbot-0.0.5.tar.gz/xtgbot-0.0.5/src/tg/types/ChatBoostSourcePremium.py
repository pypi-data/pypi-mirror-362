from .User import User
from .ChatBoostSource import ChatBoostSource
from ..base_type import base_type
from typing import Optional

@base_type
class ChatBoostSourcePremium(ChatBoostSource):
    '''
    The boost was obtained by subscribing to Telegram Premium or by gifting a Telegram Premium subscription to another user.
    '''

    user: User
    '''
    User that boosted the chat
    '''

    source: str
    '''
    Source of the boost, always "premium"
    '''

