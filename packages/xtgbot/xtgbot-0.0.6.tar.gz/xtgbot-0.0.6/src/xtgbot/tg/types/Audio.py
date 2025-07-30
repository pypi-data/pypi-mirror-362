from .PhotoSize import PhotoSize
from ..base_type import base_type
from typing import Optional

@base_type
class Audio:
    '''
    This object represents an audio file to be treated as music by the Telegram clients.
    '''

    duration: int
    '''
    Duration of the audio in seconds as defined by the sender
    '''

    file_unique_id: str
    '''
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    '''

    file_id: str
    '''
    Identifier for this file, which can be used to download or reuse the file
    '''

    performer: Optional[str] = None
    '''
    Optional. Performer of the audio as defined by the sender or by audio tags
    '''

    title: Optional[str] = None
    '''
    Optional. Title of the audio as defined by the sender or by audio tags
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

    thumbnail: Optional[PhotoSize] = None
    '''
    Optional. Thumbnail of the album cover to which the music file belongs
    '''

