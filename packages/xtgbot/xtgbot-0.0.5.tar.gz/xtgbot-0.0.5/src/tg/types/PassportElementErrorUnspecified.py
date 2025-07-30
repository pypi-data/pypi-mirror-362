from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorUnspecified(PassportElementError):
    '''
    Represents an issue in an unspecified place. The error is considered resolved when new data is added.
    '''

    message: str
    '''
    Error message
    '''

    element_hash: str
    '''
    Base64-encoded element hash
    '''

    type: str
    '''
    Type of element of the user's Telegram Passport which has the issue
    '''

    source: str
    '''
    Error source, must be unspecified
    '''

