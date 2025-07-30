from ..base_type import base_type
from typing import Optional

@base_type
class StarAmount:
    '''
    Describes an amount of Telegram Stars.
    '''

    amount: int
    '''
    Integer amount of Telegram Stars, rounded to 0; can be negative
    '''

    nanostar_amount: Optional[int] = None
    '''
    Optional. The number of 1/1000000000 shares of Telegram Stars; from -999999999 to 999999999; can be negative if and only if amount is non-positive
    '''

