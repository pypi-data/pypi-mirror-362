from ..base_type import base_type
from typing import Optional

@base_type
class ChatBoostAdded:
    '''
    This object represents a service message about a user boosting a chat.
    '''

    boost_count: int
    '''
    Number of boosts added by the user
    '''

