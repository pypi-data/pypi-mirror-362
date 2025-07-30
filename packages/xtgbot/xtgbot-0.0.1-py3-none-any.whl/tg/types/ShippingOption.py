from .LabeledPrice import LabeledPrice
from ..base_type import base_type
from typing import Optional

@base_type
class ShippingOption:
    '''
    This object represents one shipping option.
    '''

    prices: list[LabeledPrice]
    '''
    List of price portions
    '''

    title: str
    '''
    Option title
    '''

    id: str
    '''
    Shipping option identifier
    '''

