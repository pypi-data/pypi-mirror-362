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
class InlineQueryResultCachedGif(InlineQueryResult):
    '''
    Represents a link to an animated GIF file stored on the Telegram servers. By default, this animated GIF file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with specified content instead of the animation.
    '''

    gif_file_id: str
    '''
    A valid file identifier for the GIF file
    '''

    id: str
    '''
    Unique identifier for this result, 1-64 bytes
    '''

    type: str
    '''
    Type of the result, must be gif
    '''

    title: Optional[str] = None
    '''
    Optional. Title for the result
    '''

    caption: Optional[str] = None
    '''
    Optional. Caption of the GIF file to be sent, 0-1024 characters after entities parsing
    '''

    parse_mode: Optional[str] = None
    '''
    Optional. Mode for parsing entities in the caption. See formatting options for more details.
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
    Optional. Content of the message to be sent instead of the GIF animation
    '''

