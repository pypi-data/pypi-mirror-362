from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineQueryResult import InlineQueryResult
from ..base_type import base_type
from typing import Optional

@base_type
class InlineQueryResultArticle(InlineQueryResult):
    '''
    Represents a link to an article or web page.
    '''

    input_message_content: InputMessageContent
    '''
    Content of the message to be sent
    '''

    title: str
    '''
    Title of the result
    '''

    id: str
    '''
    Unique identifier for this result, 1-64 Bytes
    '''

    type: str
    '''
    Type of the result, must be article
    '''

    reply_markup: Optional[InlineKeyboardMarkup] = None
    '''
    Optional. Inline keyboard attached to the message
    '''

    url: Optional[str] = None
    '''
    Optional. URL of the result
    '''

    description: Optional[str] = None
    '''
    Optional. Short description of the result
    '''

    thumbnail_url: Optional[str] = None
    '''
    Optional. Url of the thumbnail for the result
    '''

    thumbnail_width: Optional[int] = None
    '''
    Optional. Thumbnail width
    '''

    thumbnail_height: Optional[int] = None
    '''
    Optional. Thumbnail height
    '''

