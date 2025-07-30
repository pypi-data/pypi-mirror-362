from .User import User
from .User import User
from .ChatMember import ChatMember
from ..base_type import base_type
from typing import Optional

@base_type
class ChatMemberBanned(ChatMember):
    '''
    Represents a chat member that was banned in the chat and can't return to the chat or view chat messages.
    '''

    until_date: int
    '''
    Date when restrictions will be lifted for this user; Unix time. If 0, then the user is banned forever
    '''

    user: User
    '''
    Information about the user
    '''

    status: str
    '''
    The member's status in the chat, always "kicked"
    '''

