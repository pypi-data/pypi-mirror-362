from .PhotoSize import PhotoSize
from .PaidMedia import PaidMedia
from ..base_type import base_type
from typing import Optional

@base_type
class PaidMediaPhoto(PaidMedia):
    '''
    The paid media is a photo.
    '''

    photo: list[PhotoSize]
    '''
    The photo
    '''

    type: str
    '''
    Type of the paid media, always "photo"
    '''

