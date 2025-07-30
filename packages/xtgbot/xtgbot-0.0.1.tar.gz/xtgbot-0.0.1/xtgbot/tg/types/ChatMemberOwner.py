from .User import User
from .User import User
from .User import User
from .ChatMember import ChatMember
from ..base_type import base_type
from typing import Optional

@base_type
class ChatMemberOwner(ChatMember):
    '''
    Represents a chat member that owns the chat and has all administrator privileges.
    '''

    is_anonymous: bool
    '''
    True, if the user's presence in the chat is hidden
    '''

    user: User
    '''
    Information about the user
    '''

    status: str
    '''
    The member's status in the chat, always "creator"
    '''

    custom_title: Optional[str] = None
    '''
    Optional. Custom title for this user
    '''

