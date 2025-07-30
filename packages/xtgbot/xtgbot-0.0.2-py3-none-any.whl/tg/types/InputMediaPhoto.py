from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .InputMedia import InputMedia
from ..base_type import base_type
from typing import Optional

@base_type
class InputMediaPhoto(InputMedia):
    '''
    Represents a photo to be sent.
    '''

    media: str
    '''
    File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    '''

    type: str
    '''
    Type of the result, must be photo
    '''

    caption: Optional[str] = None
    '''
    Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing
    '''

    parse_mode: Optional[str] = None
    '''
    Optional. Mode for parsing entities in the photo caption. See formatting options for more details.
    '''

    caption_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
    '''

    show_caption_above_media: bool = False
    '''
    Optional. Pass True, if the caption must be shown above the message media
    '''

    has_spoiler: bool = False
    '''
    Optional. Pass True if the photo needs to be covered with a spoiler animation
    '''

