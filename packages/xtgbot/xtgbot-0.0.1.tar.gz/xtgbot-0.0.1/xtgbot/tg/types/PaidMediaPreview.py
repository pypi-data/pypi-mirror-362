from .PaidMedia import PaidMedia
from ..base_type import base_type
from typing import Optional

@base_type
class PaidMediaPreview(PaidMedia):
    '''
    The paid media isn't available before the payment.
    '''

    type: str
    '''
    Type of the paid media, always "preview"
    '''

    width: Optional[int] = None
    '''
    Optional. Media width as defined by the sender
    '''

    height: Optional[int] = None
    '''
    Optional. Media height as defined by the sender
    '''

    duration: Optional[int] = None
    '''
    Optional. Duration of the media in seconds as defined by the sender
    '''

