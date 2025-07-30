from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InlineQueryResult import InlineQueryResult
from ..base_type import base_type
from typing import Optional

@base_type
class InlineQueryResultCachedSticker(InlineQueryResult):
    '''
    Represents a link to a sticker stored on the Telegram servers. By default, this sticker will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the sticker.
    '''

    sticker_file_id: str
    '''
    A valid file identifier of the sticker
    '''

    id: str
    '''
    Unique identifier for this result, 1-64 bytes
    '''

    type: str
    '''
    Type of the result, must be sticker
    '''

    reply_markup: Optional[InlineKeyboardMarkup] = None
    '''
    Optional. Inline keyboard attached to the message
    '''

    input_message_content: Optional[InputMessageContent] = None
    '''
    Optional. Content of the message to be sent instead of the sticker
    '''

