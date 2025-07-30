from ..base_type import base_type
from typing import Optional

@base_type
class PreparedInlineMessage:
    '''
    Describes an inline message to be sent by a user of a Mini App.
    '''

    expiration_date: int
    '''
    Expiration date of the prepared message, in Unix time. Expired prepared messages can no longer be used
    '''

    id: str
    '''
    Unique identifier of the prepared message
    '''

