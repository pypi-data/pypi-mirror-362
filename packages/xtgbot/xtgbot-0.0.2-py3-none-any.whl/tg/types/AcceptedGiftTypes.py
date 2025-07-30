from ..base_type import base_type
from typing import Optional

@base_type
class AcceptedGiftTypes:
    '''
    This object describes the types of gifts that can be gifted to a user or a chat.
    '''

    premium_subscription: bool
    '''
    True, if a Telegram Premium subscription is accepted
    '''

    unique_gifts: bool
    '''
    True, if unique gifts or gifts that can be upgraded to unique for free are accepted
    '''

    limited_gifts: bool
    '''
    True, if limited regular gifts are accepted
    '''

    unlimited_gifts: bool
    '''
    True, if unlimited regular gifts are accepted
    '''

