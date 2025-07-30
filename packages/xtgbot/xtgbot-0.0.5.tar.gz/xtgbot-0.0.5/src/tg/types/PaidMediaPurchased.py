from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class PaidMediaPurchased:
    '''
    This object contains information about a paid media purchase.
    '''

    paid_media_payload: str
    '''
    Bot-specified paid media payload
    '''

    from_: User
    '''
    User who purchased the media
    '''

