from .User import User
from .ShippingAddress import ShippingAddress
from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class ShippingQuery:
    '''
    This object contains information about an incoming shipping query.
    '''

    shipping_address: ShippingAddress
    '''
    User specified shipping address
    '''

    invoice_payload: str
    '''
    Bot-specified invoice payload
    '''

    from_: User
    '''
    User who sent the query
    '''

    id: str
    '''
    Unique query identifier
    '''

