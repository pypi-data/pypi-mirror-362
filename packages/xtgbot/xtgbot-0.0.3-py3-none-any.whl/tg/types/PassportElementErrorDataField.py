from .PassportElementError import PassportElementError
from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementErrorDataField(PassportElementError):
    '''
    Represents an issue in one of the data fields that was provided by the user. The error is considered resolved when the field's value changes.
    '''

    message: str
    '''
    Error message
    '''

    data_hash: str
    '''
    Base64-encoded data hash
    '''

    field_name: str
    '''
    Name of the data field which has the error
    '''

    type: str
    '''
    The section of the user's Telegram Passport which has the error, one of "personal_details", "passport", "driver_license", "identity_card", "internal_passport", "address"
    '''

    source: str
    '''
    Error source, must be data
    '''

