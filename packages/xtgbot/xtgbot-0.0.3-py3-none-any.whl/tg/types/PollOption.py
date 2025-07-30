from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from ..base_type import base_type
from typing import Optional

@base_type
class PollOption:
    '''
    This object contains information about one answer option in a poll.
    '''

    voter_count: int
    '''
    Number of users that voted for this option
    '''

    text: str
    '''
    Option text, 1-100 characters
    '''

    text_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. Special entities that appear in the option text. Currently, only custom emoji entities are allowed in poll option texts
    '''

