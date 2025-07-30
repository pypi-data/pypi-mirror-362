from .User import User
from .ChatMember import ChatMember
from ..base_type import base_type
from typing import Optional

@base_type
class ChatMemberLeft(ChatMember):
    '''
    Represents a chat member that isn't currently a member of the chat, but may join it themselves.
    '''

    user: User
    '''
    Information about the user
    '''

    status: str
    '''
    The member's status in the chat, always "left"
    '''

