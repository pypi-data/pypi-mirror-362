from .Chat import Chat
from .Chat import Chat
from .MessageOrigin import MessageOrigin
from ..base_type import base_type
from typing import Optional

@base_type
class MessageOriginChat(MessageOrigin):
    '''
    The message was originally sent on behalf of a chat to a group chat.
    '''

    sender_chat: Chat
    '''
    Chat that sent the message originally
    '''

    date: int
    '''
    Date the message was sent originally in Unix time
    '''

    type: str
    '''
    Type of the message origin, always "chat"
    '''

    author_signature: Optional[str] = None
    '''
    Optional. For messages originally sent by an anonymous chat administrator, original message author signature
    '''

