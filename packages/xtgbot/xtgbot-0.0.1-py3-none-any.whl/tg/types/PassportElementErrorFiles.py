from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorFiles(PassportElementError):
    '''
    Represents an issue with a list of scans. The error is considered resolved when the list of files containing the scans changes.
    '''

    message: str
    '''
    Error message
    '''

    file_hashes: list[str]
    '''
    List of base64-encoded file hashes
    '''

    type: str
    '''
    The section of the user's Telegram Passport which has the issue, one of "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration"
    '''

    source: str
    '''
    Error source, must be files
    '''

