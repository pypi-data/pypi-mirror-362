from ..base_type import base_type
from typing import Optional

@base_type
class ShippingAddress:
    '''
    This object represents a shipping address.
    '''

    post_code: str
    '''
    Address post code
    '''

    street_line2: str
    '''
    Second line for the address
    '''

    street_line1: str
    '''
    First line for the address
    '''

    city: str
    '''
    City
    '''

    state: str
    '''
    State, if applicable
    '''

    country_code: str
    '''
    Two-letter ISO 3166-1 alpha-2 country code
    '''

