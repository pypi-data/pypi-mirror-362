from ..base_type import base_type
from typing import Optional

@base_type
class ForumTopicCreated:
    '''
    This object represents a service message about a new forum topic created in the chat.
    '''

    icon_color: int
    '''
    Color of the topic icon in RGB format
    '''

    name: str
    '''
    Name of the topic
    '''

    icon_custom_emoji_id: Optional[str] = None
    '''
    Optional. Unique identifier of the custom emoji shown as the topic icon
    '''

