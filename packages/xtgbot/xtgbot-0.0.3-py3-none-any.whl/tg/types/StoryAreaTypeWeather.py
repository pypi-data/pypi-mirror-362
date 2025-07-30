from .StoryAreaType import StoryAreaType
from ..base_type import base_type
from typing import Optional

@base_type
class StoryAreaTypeWeather(StoryAreaType):
    '''
    Describes a story area containing weather information. Currently, a story can have up to 3 weather areas.
    '''

    background_color: int
    '''
    A color of the area background in the ARGB format
    '''

    emoji: str
    '''
    Emoji representing the weather
    '''

    temperature: float
    '''
    Temperature, in degree Celsius
    '''

    type: str
    '''
    Type of the area, always "weather"
    '''

