from ..base_type import base_type
from typing import Optional

@base_type
class MessageAutoDeleteTimerChanged:
    '''
    This object represents a service message about a change in auto-delete timer settings.
    '''

    message_auto_delete_time: int
    '''
    New auto-delete time for messages in the chat; in seconds
    '''

