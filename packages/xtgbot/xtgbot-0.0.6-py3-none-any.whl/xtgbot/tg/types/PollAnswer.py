from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class PollAnswer:
    '''
    This object represents an answer of a user in a non-anonymous poll.
    '''

    option_ids: list[int]
    '''
    0-based identifiers of chosen answer options. May be empty if the vote was retracted.
    '''

    poll_id: str
    '''
    Unique poll identifier
    '''

    voter_chat: Optional[Chat] = None
    '''
    Optional. The chat that changed the answer to the poll, if the voter is anonymous
    '''

    user: Optional[User] = None
    '''
    Optional. The user that changed the answer to the poll, if the voter isn't anonymous
    '''

