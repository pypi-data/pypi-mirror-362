from ..base_type import base_type
from typing import Optional

@base_type
class VideoChatEnded:
    '''
    This object represents a service message about a video chat ended in the chat.
    '''

    duration: int
    '''
    Video chat duration in seconds
    '''

