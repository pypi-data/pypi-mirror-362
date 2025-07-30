from ..base_type import base_type
from typing import Optional

@base_type
class LocationAddress:
    '''
    Describes the physical address of a location.
    '''

    country_code: str
    '''
    The two-letter ISO 3166-1 alpha-2 country code of the country where the location is located
    '''

    state: Optional[str] = None
    '''
    Optional. State of the location
    '''

    city: Optional[str] = None
    '''
    Optional. City of the location
    '''

    street: Optional[str] = None
    '''
    Optional. Street address of the location
    '''

