from ..base_type import base_type
from typing import Optional

@base_type
class ForumTopicEdited:
    '''
    This object represents a service message about an edited forum topic.
    '''

    name: Optional[str] = None
    '''
    Optional. New name of the topic, if it was edited
    '''

    icon_custom_emoji_id: Optional[str] = None
    '''
    Optional. New identifier of the custom emoji shown as the topic icon, if it was edited; an empty string if the icon was removed
    '''

