from .Gift import Gift
from ..base_type import base_type
from typing import Optional

@base_type
class Gifts:
    '''
    This object represent a list of gifts.
    '''

    gifts: list[Gift]
    '''
    The list of gifts
    '''

