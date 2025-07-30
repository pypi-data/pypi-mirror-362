from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorSelfie(PassportElementError):
    '''
    Represents an issue with the selfie with a document. The error is considered resolved when the file with the selfie changes.
    '''

    message: str
    '''
    Error message
    '''

    file_hash: str
    '''
    Base64-encoded hash of the file with the selfie
    '''

    type: str
    '''
    The section of the user's Telegram Passport which has the issue, one of "passport", "driver_license", "identity_card", "internal_passport"
    '''

    source: str
    '''
    Error source, must be selfie
    '''

