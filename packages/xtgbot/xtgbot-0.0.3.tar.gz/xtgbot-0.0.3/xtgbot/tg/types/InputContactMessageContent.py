from .InputMessageContent import InputMessageContent
from ..base_type import base_type
from typing import Optional

@base_type
class InputContactMessageContent(InputMessageContent):
    '''
    Represents the content of a contact message to be sent as the result of an inline query.
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

    vcard: Optional[str] = None
    '''
    Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes
    '''

