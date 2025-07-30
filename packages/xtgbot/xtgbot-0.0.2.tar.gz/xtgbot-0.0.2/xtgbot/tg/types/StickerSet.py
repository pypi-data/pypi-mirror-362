from .Sticker import Sticker
from .PhotoSize import PhotoSize
from .Sticker import Sticker
from ..base_type import base_type
from typing import Optional

@base_type
class StickerSet:
    '''
    This object represents a sticker set.
    '''

    stickers: list[Sticker]
    '''
    List of all set stickers
    '''

    sticker_type: str
    '''
    Type of stickers in the set, currently one of "regular", "mask", "custom_emoji"
    '''

    title: str
    '''
    Sticker set title
    '''

    name: str
    '''
    Sticker set name
    '''

    thumbnail: Optional[PhotoSize] = None
    '''
    Optional. Sticker set thumbnail in the .WEBP, .TGS, or .WEBM format
    '''

