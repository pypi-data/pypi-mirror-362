from .MessageEntity import MessageEntity
from ..base_type import base_type
from typing import Optional

@base_type
class InputPollOption:
    '''
    This object contains information about one answer option in a poll to be sent.
    '''

    text: str
    '''
    Option text, 1-100 characters
    '''

    text_parse_mode: Optional[str] = None
    '''
    Optional. Mode for parsing entities in the text. See formatting options for more details. Currently, only custom emoji entities are allowed
    '''

    text_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. A JSON-serialized list of special entities that appear in the poll option text. It can be specified instead of text_parse_mode
    '''

