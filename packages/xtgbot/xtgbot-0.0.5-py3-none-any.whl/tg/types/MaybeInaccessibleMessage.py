from ..base_type import base_type
from .InaccessibleMessage import InaccessibleMessage
from .Message import Message
from typing import Optional

@base_type
class MaybeInaccessibleMessage(InaccessibleMessage, Message):
    '''
    This object describes a message that can be inaccessible to the bot. It can be one of
    - Message
    - InaccessibleMessage
    '''

    pass
