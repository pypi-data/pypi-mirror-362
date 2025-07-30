from ..base_type import base_type
from typing import Optional

@base_type
class Chat:
    '''
    This object represents a chat.
    '''

    type: str
    '''
    Type of the chat, can be either "private", "group", "supergroup" or "channel"
    '''

    id: int
    '''
    Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
    '''

    title: Optional[str] = None
    '''
    Optional. Title, for supergroups, channels and group chats
    '''

    username: Optional[str] = None
    '''
    Optional. Username, for private chats, supergroups and channels if available
    '''

    first_name: Optional[str] = None
    '''
    Optional. First name of the other party in a private chat
    '''

    last_name: Optional[str] = None
    '''
    Optional. Last name of the other party in a private chat
    '''

    is_forum: bool = False
    '''
    Optional. True, if the supergroup chat is a forum (has topics enabled)
    '''

