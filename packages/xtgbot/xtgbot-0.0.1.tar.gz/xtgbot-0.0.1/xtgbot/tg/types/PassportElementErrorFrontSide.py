from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorFrontSide(PassportElementError):
    '''
    Represents an issue with the front side of a document. The error is considered resolved when the file with the front side of the document changes.
    '''

    message: str
    '''
    Error message
    '''

    file_hash: str
    '''
    Base64-encoded hash of the file with the front side of the document
    '''

    type: str
    '''
    The section of the user's Telegram Passport which has the issue, one of "passport", "driver_license", "identity_card", "internal_passport"
    '''

    source: str
    '''
    Error source, must be front_side
    '''

