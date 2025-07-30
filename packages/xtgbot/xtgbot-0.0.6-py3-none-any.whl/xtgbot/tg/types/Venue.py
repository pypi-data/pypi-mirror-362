from .Location import Location
from .Location import Location
from .Location import Location
from .Location import Location
from .Location import Location
from .Location import Location
from .Location import Location
from ..base_type import base_type
from typing import Optional

@base_type
class Venue:
    '''
    This object represents a venue.
    '''

    address: str
    '''
    Address of the venue
    '''

    title: str
    '''
    Name of the venue
    '''

    location: Location
    '''
    Venue location. Can't be a live location
    '''

    foursquare_id: Optional[str] = None
    '''
    Optional. Foursquare identifier of the venue
    '''

    foursquare_type: Optional[str] = None
    '''
    Optional. Foursquare type of the venue. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
    '''

    google_place_id: Optional[str] = None
    '''
    Optional. Google Places identifier of the venue
    '''

    google_place_type: Optional[str] = None
    '''
    Optional. Google Places type of the venue. (See supported types.)
    '''

