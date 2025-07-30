from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorFile(PassportElementError):
    '''
    Represents an issue with a document scan. The error is considered resolved when the file with the document scan changes.
    '''

    message: str
    '''
    Error message
    '''

    file_hash: str
    '''
    Base64-encoded file hash
    '''

    type: str
    '''
    The section of the user's Telegram Passport which has the issue, one of "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration"
    '''

    source: str
    '''
    Error source, must be file
    '''

