from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorReverseSide(PassportElementError):
    '''
    Represents an issue with the reverse side of a document. The error is considered resolved when the file with reverse side of the document changes.
    '''

    message: str
    '''
    Error message
    '''

    file_hash: str
    '''
    Base64-encoded hash of the file with the reverse side of the document
    '''

    type: str
    '''
    The section of the user's Telegram Passport which has the issue, one of "driver_license", "identity_card"
    '''

    source: str
    '''
    Error source, must be reverse_side
    '''

