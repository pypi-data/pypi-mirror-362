from .Chat import Chat
from .User import User
from .ChatInviteLink import ChatInviteLink
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class ChatJoinRequest:
    '''
    Represents a join request sent to a chat.
    '''

    date: int
    '''
    Date the request was sent in Unix time
    '''

    user_chat_id: int
    '''
    Identifier of a private chat with the user who sent the join request. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier. The bot can use this identifier for 5 minutes to send messages until the join request is processed, assuming no other administrator contacted the user.
    '''

    from_: User
    '''
    User that sent the join request
    '''

    chat: Chat
    '''
    Chat to which the request was sent
    '''

    bio: Optional[str] = None
    '''
    Optional. Bio of the user.
    '''

    invite_link: Optional[ChatInviteLink] = None
    '''
    Optional. Chat invite link that was used by the user to send the join request
    '''

