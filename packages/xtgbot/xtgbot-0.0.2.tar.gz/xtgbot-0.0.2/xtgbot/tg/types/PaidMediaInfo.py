from .PaidMedia import PaidMedia
from ..base_type import base_type
from typing import Optional

@base_type
class PaidMediaInfo:
    '''
    Describes the paid media added to a message.
    '''

    paid_media: list[PaidMedia]
    '''
    Information about the paid media
    '''

    star_count: int
    '''
    The number of Telegram Stars that must be paid to buy access to the media
    '''

