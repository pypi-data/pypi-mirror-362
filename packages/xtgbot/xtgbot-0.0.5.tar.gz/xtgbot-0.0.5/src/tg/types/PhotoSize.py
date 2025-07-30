from ..base_type import base_type
from typing import Optional

@base_type
class PhotoSize:
    '''
    This object represents one size of a photo or a file / sticker thumbnail.
    '''

    height: int
    '''
    Photo height
    '''

    width: int
    '''
    Photo width
    '''

    file_unique_id: str
    '''
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    '''

    file_id: str
    '''
    Identifier for this file, which can be used to download or reuse the file
    '''

    file_size: Optional[int] = None
    '''
    Optional. File size in bytes
    '''

