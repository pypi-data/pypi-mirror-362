from .User import User
from .BusinessBotRights import BusinessBotRights
from .User import User
from .BusinessBotRights import BusinessBotRights
from .User import User
from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class BusinessConnection:
    '''
    Describes the connection of the bot with a business account.
    '''

    is_enabled: bool
    '''
    True, if the connection is active
    '''

    date: int
    '''
    Date the connection was established in Unix time
    '''

    user_chat_id: int
    '''
    Identifier of a private chat with the user who created the business connection. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
    '''

    user: User
    '''
    Business account user that created the business connection
    '''

    id: str
    '''
    Unique identifier of the business connection
    '''

    rights: Optional[BusinessBotRights] = None
    '''
    Optional. Rights of the business bot
    '''

