from .PhotoSize import PhotoSize
from .File import File
from .MaskPosition import MaskPosition
from .PhotoSize import PhotoSize
from .File import File
from .MaskPosition import MaskPosition
from .PhotoSize import PhotoSize
from .File import File
from .MaskPosition import MaskPosition
from .PhotoSize import PhotoSize
from .File import File
from .MaskPosition import MaskPosition
from .PhotoSize import PhotoSize
from .File import File
from .PhotoSize import PhotoSize
from .PhotoSize import PhotoSize
from .PhotoSize import PhotoSize
from ..base_type import base_type
from typing import Optional

@base_type
class Sticker:
    '''
    This object represents a sticker.
    '''

    is_video: bool
    '''
    True, if the sticker is a video sticker
    '''

    is_animated: bool
    '''
    True, if the sticker is animated
    '''

    height: int
    '''
    Sticker height
    '''

    width: int
    '''
    Sticker width
    '''

    type: str
    '''
    Type of the sticker, currently one of "regular", "mask", "custom_emoji". The type of the sticker is independent from its format, which is determined by the fields is_animated and is_video.
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
    Optional. Sticker thumbnail in the .WEBP or .JPG format
    '''

    thumb: Optional[PhotoSize] = None
    '''
    Optional. Sticker thumbnail in the .WEBP or .JPG format
    '''

    emoji: Optional[str] = None
    '''
    Optional. Emoji associated with the sticker
    '''

    set_name: Optional[str] = None
    '''
    Optional. Name of the sticker set to which the sticker belongs
    '''

    premium_animation: Optional[File] = None
    '''
    Optional. For premium regular stickers, premium animation for the sticker
    '''

    mask_position: Optional[MaskPosition] = None
    '''
    Optional. For mask stickers, the position where the mask should be placed
    '''

    custom_emoji_id: Optional[str] = None
    '''
    Optional. For custom emoji stickers, unique identifier of the custom emoji
    '''

    needs_repainting: bool = False
    '''
    Optional. True, if the sticker must be repainted to a text color in messages, the color of the Telegram Premium badge in emoji status, white color on chat photos, or another appropriate color in other places
    '''

    file_size: Optional[int] = None
    '''
    Optional. File size in bytes
    '''

