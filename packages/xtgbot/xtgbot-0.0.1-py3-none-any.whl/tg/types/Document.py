from .PhotoSize import PhotoSize
from .PhotoSize import PhotoSize
from .PhotoSize import PhotoSize
from .PhotoSize import PhotoSize
from ..base_type import base_type
from typing import Optional

@base_type
class Document:
    '''
    This object represents a general file (as opposed to photos, voice messages and audio files).
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
    Optional. Document thumbnail as defined by the sender
    '''

    file_name: Optional[str] = None
    '''
    Optional. Original filename as defined by the sender
    '''

    mime_type: Optional[str] = None
    '''
    Optional. MIME type of the file as defined by the sender
    '''

    file_size: Optional[int] = None
    '''
    Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value.
    '''

