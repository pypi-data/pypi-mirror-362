from .User import User
from .User import User
from .ChatMember import ChatMember
from ..base_type import base_type
from typing import Optional

@base_type
class ChatMemberMember(ChatMember):
    '''
    Represents a chat member that has no additional privileges or restrictions.
    '''

    user: User
    '''
    Information about the user
    '''

    status: str
    '''
    The member's status in the chat, always "member"
    '''

    until_date: Optional[int] = None
    '''
    Optional. Date when the user's subscription will expire; Unix time
    '''

