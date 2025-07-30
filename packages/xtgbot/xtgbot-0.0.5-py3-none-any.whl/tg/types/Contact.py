from ..base_type import base_type
from typing import Optional

@base_type
class Contact:
    '''
    This object represents a phone contact.
    '''

    first_name: str
    '''
    Contact's first name
    '''

    phone_number: str
    '''
    Contact's phone number
    '''

    last_name: Optional[str] = None
    '''
    Optional. Contact's last name
    '''

    user_id: Optional[int] = None
    '''
    Optional. Contact's user identifier in Telegram. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
    '''

    vcard: Optional[str] = None
    '''
    Optional. Additional data about the contact in the form of a vCard
    '''

