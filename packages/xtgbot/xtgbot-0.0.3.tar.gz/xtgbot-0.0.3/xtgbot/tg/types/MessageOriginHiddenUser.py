from .MessageOrigin import MessageOrigin
from ..base_type import base_type
from typing import Optional

@base_type
class MessageOriginHiddenUser(MessageOrigin):
    '''
    The message was originally sent by an unknown user.
    '''

    sender_user_name: str
    '''
    Name of the user that sent the message originally
    '''

    date: int
    '''
    Date the message was sent originally in Unix time
    '''

    type: str
    '''
    Type of the message origin, always "hidden_user"
    '''

