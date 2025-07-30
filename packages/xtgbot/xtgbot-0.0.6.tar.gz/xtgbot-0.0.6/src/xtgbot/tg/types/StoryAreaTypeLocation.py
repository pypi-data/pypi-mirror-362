from .LocationAddress import LocationAddress
from .StoryAreaType import StoryAreaType
from ..base_type import base_type
from typing import Optional

@base_type
class StoryAreaTypeLocation(StoryAreaType):
    '''
    Describes a story area pointing to a location. Currently, a story can have up to 10 location areas.
    '''

    longitude: float
    '''
    Location longitude in degrees
    '''

    latitude: float
    '''
    Location latitude in degrees
    '''

    type: str
    '''
    Type of the area, always "location"
    '''

    address: Optional[LocationAddress] = None
    '''
    Optional. Address of the location
    '''

