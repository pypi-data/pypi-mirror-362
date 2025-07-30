from .StoryAreaType import StoryAreaType
from ..base_type import base_type
from typing import Optional

@base_type
class StoryAreaTypeLink(StoryAreaType):
    '''
    Describes a story area pointing to an HTTP or tg:// link. Currently, a story can have up to 3 link areas.
    '''

    url: str
    '''
    HTTP or tg:// URL to be opened when the area is clicked
    '''

    type: str
    '''
    Type of the area, always "link"
    '''

