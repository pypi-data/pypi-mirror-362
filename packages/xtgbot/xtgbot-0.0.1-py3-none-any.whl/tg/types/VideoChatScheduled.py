from ..base_type import base_type
from typing import Optional

@base_type
class VideoChatScheduled:
    '''
    This object represents a service message about a video chat scheduled in the chat.
    '''

    start_date: int
    '''
    Point in time (Unix timestamp) when the video chat is supposed to be started by a chat administrator
    '''

