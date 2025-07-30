from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
# from .MaybeInaccessibleMessage import MaybeInaccessibleMessage
from ..base_type import base_type
from typing import Optional

@base_type
class InaccessibleMessage:
    '''
    This object describes a message that was deleted or is otherwise inaccessible to the bot.
    '''

    date: int
    '''
    Always 0. The field can be used to differentiate regular and inaccessible messages.
    '''

    message_id: int
    '''
    Unique message identifier inside the chat
    '''

    chat: Chat
    '''
    Chat the message belonged to
    '''

