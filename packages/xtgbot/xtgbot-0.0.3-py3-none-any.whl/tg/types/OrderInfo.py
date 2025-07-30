from .ShippingAddress import ShippingAddress
from ..base_type import base_type
from typing import Optional

@base_type
class OrderInfo:
    '''
    This object represents information about an order.
    '''

    name: Optional[str] = None
    '''
    Optional. User name
    '''

    phone_number: Optional[str] = None
    '''
    Optional. User's phone number
    '''

    email: Optional[str] = None
    '''
    Optional. User email
    '''

    shipping_address: Optional[ShippingAddress] = None
    '''
    Optional. User shipping address
    '''

