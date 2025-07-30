from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InlineQueryResult import InlineQueryResult
from ..base_type import base_type
from typing import Optional

@base_type
class InlineQueryResultContact(InlineQueryResult):
    '''
    Represents a contact with a phone number. By default, this contact will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the contact.
    '''

    first_name: str
    '''
    Contact's first name
    '''

    phone_number: str
    '''
    Contact's phone number
    '''

    id: str
    '''
    Unique identifier for this result, 1-64 Bytes
    '''

    type: str
    '''
    Type of the result, must be contact
    '''

    last_name: Optional[str] = None
    '''
    Optional. Contact's last name
    '''

    vcard: Optional[str] = None
    '''
    Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes
    '''

    reply_markup: Optional[InlineKeyboardMarkup] = None
    '''
    Optional. Inline keyboard attached to the message
    '''

    input_message_content: Optional[InputMessageContent] = None
    '''
    Optional. Content of the message to be sent instead of the contact
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

