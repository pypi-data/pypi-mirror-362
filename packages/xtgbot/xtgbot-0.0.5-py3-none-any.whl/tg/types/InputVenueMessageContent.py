from .InputMessageContent import InputMessageContent
from ..base_type import base_type
from typing import Optional

@base_type
class InputVenueMessageContent(InputMessageContent):
    '''
    Represents the content of a venue message to be sent as the result of an inline query.
    '''

    address: str
    '''
    Address of the venue
    '''

    title: str
    '''
    Name of the venue
    '''

    longitude: float
    '''
    Longitude of the venue in degrees
    '''

    latitude: float
    '''
    Latitude of the venue in degrees
    '''

    foursquare_id: Optional[str] = None
    '''
    Optional. Foursquare identifier of the venue, if known
    '''

    foursquare_type: Optional[str] = None
    '''
    Optional. Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
    '''

    google_place_id: Optional[str] = None
    '''
    Optional. Google Places identifier of the venue
    '''

    google_place_type: Optional[str] = None
    '''
    Optional. Google Places type of the venue. (See supported types.)
    '''

