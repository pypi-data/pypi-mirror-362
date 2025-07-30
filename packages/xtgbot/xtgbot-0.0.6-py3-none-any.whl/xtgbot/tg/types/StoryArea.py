from .StoryAreaType import StoryAreaType
from .StoryAreaPosition import StoryAreaPosition
from .StoryAreaPosition import StoryAreaPosition
from ..base_type import base_type
from typing import Optional

@base_type
class StoryArea:
    '''
    Describes a clickable area on a story media.
    '''

    type: StoryAreaType
    '''
    Type of the area
    '''

    position: StoryAreaPosition
    '''
    Position of the area
    '''

