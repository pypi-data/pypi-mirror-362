from .User import User
from .MessageOrigin import MessageOrigin
from ..base_type import base_type
from typing import Optional

@base_type
class MessageOriginUser(MessageOrigin):
    '''
    The message was originally sent by a known user.
    '''

    sender_user: User
    '''
    User that sent the message originally
    '''

    date: int
    '''
    Date the message was sent originally in Unix time
    '''

    type: str
    '''
    Type of the message origin, always "user"
    '''

