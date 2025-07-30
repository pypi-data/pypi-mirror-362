from .Location import Location
from ..base_type import base_type
from typing import Optional

@base_type
class BusinessLocation:
    '''
    Contains information about the location of a Telegram Business account.
    '''

    address: str
    '''
    Address of the business
    '''

    location: Optional[Location] = None
    '''
    Optional. Location of the business
    '''

