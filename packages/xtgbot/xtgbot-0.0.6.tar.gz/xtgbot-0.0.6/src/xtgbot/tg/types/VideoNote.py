from .PhotoSize import PhotoSize
from .PhotoSize import PhotoSize
from ..base_type import base_type
from typing import Optional

@base_type
class VideoNote:
    '''
    This object represents a video message (available in Telegram apps as of v.4.0).
    '''

    duration: int
    '''
    Duration of the video in seconds as defined by the sender
    '''

    length: int
    '''
    Video width and height (diameter of the video message) as defined by the sender
    '''

    file_unique_id: str
    '''
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    '''

    file_id: str
    '''
    Identifier for this file, which can be used to download or reuse the file
    '''

    thumbnail: Optional[PhotoSize] = None
    '''
    Optional. Video thumbnail
    '''

    file_size: Optional[int] = None
    '''
    Optional. File size in bytes
    '''

