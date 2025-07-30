from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from .MessageOrigin import MessageOrigin
from ..base_type import base_type
from typing import Optional

@base_type
class MessageOriginChannel(MessageOrigin):
    '''
    The message was originally sent to a channel chat.
    '''

    message_id: int
    '''
    Unique message identifier inside the chat
    '''

    chat: Chat
    '''
    Channel chat to which the message was originally sent
    '''

    date: int
    '''
    Date the message was sent originally in Unix time
    '''

    type: str
    '''
    Type of the message origin, always "channel"
    '''

    author_signature: Optional[str] = None
    '''
    Optional. Signature of the original post author
    '''

