from .User import User
from .ChatBoostSource import ChatBoostSource
from ..base_type import base_type
from typing import Optional

@base_type
class ChatBoostSourceGiftCode(ChatBoostSource):
    '''
    The boost was obtained by the creation of Telegram Premium gift codes to boost a chat. Each such code boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription.
    '''

    user: User
    '''
    User for which the gift code was created
    '''

    source: str
    '''
    Source of the boost, always "gift_code"
    '''

