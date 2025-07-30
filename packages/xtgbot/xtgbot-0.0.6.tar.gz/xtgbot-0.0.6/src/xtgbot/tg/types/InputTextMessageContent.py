from .LinkPreviewOptions import LinkPreviewOptions
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .InputMessageContent import InputMessageContent
from ..base_type import base_type
from typing import Optional

@base_type
class InputTextMessageContent(InputMessageContent):
    '''
    Represents the content of a text message to be sent as the result of an inline query.
    '''

    message_text: str
    '''
    Text of the message to be sent, 1-4096 characters
    '''

    parse_mode: Optional[str] = None
    '''
    Optional. Mode for parsing entities in the message text. See formatting options for more details.
    '''

    entities: Optional[list[MessageEntity]] = None
    '''
    Optional. List of special entities that appear in message text, which can be specified instead of parse_mode
    '''

    link_preview_options: Optional[LinkPreviewOptions] = None
    '''
    Optional. Link preview generation options for the message
    '''

