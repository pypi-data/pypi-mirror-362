from ..base_type import base_type
from typing import Optional

@base_type
class Location:
    '''
    This object represents a point on the map.
    '''

    longitude: float
    '''
    Longitude as defined by the sender
    '''

    latitude: float
    '''
    Latitude as defined by the sender
    '''

    horizontal_accuracy: Optional[float] = None
    '''
    Optional. The radius of uncertainty for the location, measured in meters; 0-1500
    '''

    live_period: Optional[int] = None
    '''
    Optional. Time relative to the message sending date, during which the location can be updated; in seconds. For active live locations only.
    '''

    heading: Optional[int] = None
    '''
    Optional. The direction in which user is moving, in degrees; 1-360. For active live locations only.
    '''

    proximity_alert_radius: Optional[int] = None
    '''
    Optional. The maximum distance for proximity alerts about approaching another chat member, in meters. For sent live locations only.
    '''

