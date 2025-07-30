from .ChatBoost import ChatBoost
from ..base_type import base_type
from typing import Optional

@base_type
class UserChatBoosts:
    '''
    This object represents a list of boosts added to a chat by a user.
    '''

    boosts: list[ChatBoost]
    '''
    The list of boosts added to the chat by the user
    '''

