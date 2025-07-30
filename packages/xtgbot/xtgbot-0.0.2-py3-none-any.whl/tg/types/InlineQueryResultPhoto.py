from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .MessageEntity import MessageEntity
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .InlineQueryResult import InlineQueryResult
from ..base_type import base_type
from typing import Optional

@base_type
class InlineQueryResultPhoto(InlineQueryResult):
    '''
    Represents a link to a photo. By default, this photo will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.
    '''

    thumbnail_url: str
    '''
    URL of the thumbnail for the photo
    '''

    photo_url: str
    '''
    A valid URL of the photo. Photo must be in JPEG format. Photo size must not exceed 5MB
    '''

    id: str
    '''
    Unique identifier for this result, 1-64 bytes
    '''

    type: str
    '''
    Type of the result, must be photo
    '''

    photo_width: Optional[int] = None
    '''
    Optional. Width of the photo
    '''

    photo_height: Optional[int] = None
    '''
    Optional. Height of the photo
    '''

    title: Optional[str] = None
    '''
    Optional. Title for the result
    '''

    description: Optional[str] = None
    '''
    Optional. Short description of the result
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

    reply_markup: Optional[InlineKeyboardMarkup] = None
    '''
    Optional. Inline keyboard attached to the message
    '''

    input_message_content: Optional[InputMessageContent] = None
    '''
    Optional. Content of the message to be sent instead of the photo
    '''

