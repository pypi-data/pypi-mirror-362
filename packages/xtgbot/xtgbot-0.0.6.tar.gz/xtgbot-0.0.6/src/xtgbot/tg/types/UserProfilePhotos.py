from .PhotoSize import PhotoSize
from ..base_type import base_type
from typing import Optional

@base_type
class UserProfilePhotos:
    '''
    This object represent a user's profile pictures.
    '''

    photos: list[list[PhotoSize]]
    '''
    Requested profile pictures (in up to 4 sizes each)
    '''

    total_count: int
    '''
    Total number of profile pictures the target user has
    '''

