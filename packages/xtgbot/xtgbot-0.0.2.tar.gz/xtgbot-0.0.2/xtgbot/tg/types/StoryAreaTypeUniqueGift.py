from .StoryAreaType import StoryAreaType
from ..base_type import base_type
from typing import Optional

@base_type
class StoryAreaTypeUniqueGift(StoryAreaType):
    '''
    Describes a story area pointing to a unique gift. Currently, a story can have at most 1 unique gift area.
    '''

    name: str
    '''
    Unique name of the gift
    '''

    type: str
    '''
    Type of the area, always "unique_gift"
    '''

