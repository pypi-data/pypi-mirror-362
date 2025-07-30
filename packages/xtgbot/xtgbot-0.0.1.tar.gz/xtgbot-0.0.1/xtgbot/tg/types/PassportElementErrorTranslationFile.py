from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorTranslationFile(PassportElementError):
    '''
    Represents an issue with one of the files that constitute the translation of a document. The error is considered resolved when the file changes.
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
    Type of element of the user's Telegram Passport which has the issue, one of "passport", "driver_license", "identity_card", "internal_passport", "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration"
    '''

    source: str
    '''
    Error source, must be translation_file
    '''

