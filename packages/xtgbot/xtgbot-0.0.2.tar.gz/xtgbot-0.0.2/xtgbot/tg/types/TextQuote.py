from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from ..base_type import base_type
from typing import Optional

@base_type
class TextQuote:
    '''
    This object contains information about the quoted part of a message that is replied to by the given message.
    '''

    position: int
    '''
    Approximate quote position in the original message in UTF-16 code units as specified by the sender
    '''

    text: str
    '''
    Text of the quoted part of a message that is replied to by the given message
    '''

    entities: Optional[list[MessageEntity]] = None
    '''
    Optional. Special entities that appear in the quote. Currently, only bold, italic, underline, strikethrough, spoiler, and custom_emoji entities are kept in quotes.
    '''

    is_manual: bool = False
    '''
    Optional. True, if the quote was chosen manually by the message sender. Otherwise, the quote was added automatically by the server.
    '''

