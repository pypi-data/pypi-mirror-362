from ..base_type import base_type
from typing import Optional

@base_type
class ForumTopic:
    '''
    This object represents a forum topic.
    '''

    icon_color: int
    '''
    Color of the topic icon in RGB format
    '''

    name: str
    '''
    Name of the topic
    '''

    message_thread_id: int
    '''
    Unique identifier of the forum topic
    '''

    icon_custom_emoji_id: Optional[str] = None
    '''
    Optional. Unique identifier of the custom emoji shown as the topic icon
    '''

