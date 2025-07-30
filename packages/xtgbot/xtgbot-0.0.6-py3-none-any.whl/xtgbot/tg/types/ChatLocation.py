from .Location import Location
from .Location import Location
from ..base_type import base_type
from typing import Optional

@base_type
class ChatLocation:
    '''
    Represents a location to which a chat is connected.
    '''

    address: str
    '''
    Location address; 1-64 characters, as defined by the chat owner
    '''

    location: Location
    '''
    The location to which the supergroup is connected. Can't be a live location.
    '''

