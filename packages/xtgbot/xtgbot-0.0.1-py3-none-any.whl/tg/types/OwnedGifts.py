from .OwnedGift import OwnedGift
from .OwnedGift import OwnedGift
from ..base_type import base_type
from typing import Optional

@base_type
class OwnedGifts:
    '''
    Contains the list of gifts received and owned by a user or a chat.
    '''

    gifts: list[OwnedGift]
    '''
    The list of gifts
    '''

    total_count: int
    '''
    The total number of gifts owned by the user or the chat
    '''

    next_offset: Optional[str] = None
    '''
    Optional. Offset for the next request. If empty, then there are no more results
    '''

