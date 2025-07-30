from .MaskPosition import MaskPosition
from .MaskPosition import MaskPosition
from ..base_type import base_type
from typing import Optional

@base_type
class InputSticker:
    '''
    This object describes a sticker to be added to a sticker set.
    '''

    emoji_list: list[str]
    '''
    List of 1-20 emoji associated with the sticker
    '''

    format: str
    '''
    Format of the added sticker, must be one of "static" for a .WEBP or .PNG image, "animated" for a .TGS animation, "video" for a .WEBM video
    '''

    sticker: str
    '''
    The added sticker. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new file using multipart/form-data under <file_attach_name> name. Animated and video stickers can't be uploaded via HTTP URL. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    '''

    mask_position: Optional[MaskPosition] = None
    '''
    Optional. Position where the mask should be placed on faces. For "mask" stickers only.
    '''

    keywords: Optional[list[str]] = None
    '''
    Optional. List of 0-20 search keywords for the sticker with total length of up to 64 characters. For "regular" and "custom_emoji" stickers only.
    '''

