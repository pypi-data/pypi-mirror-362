from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorTranslationFiles(PassportElementError):
    '''
    Represents an issue with the translated version of a document. The error is considered resolved when a file with the document translation change.
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
    Type of element of the user's Telegram Passport which has the issue, one of "passport", "driver_license", "identity_card", "internal_passport", "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration"
    '''

    source: str
    '''
    Error source, must be translation_files
    '''

