from ..base_type import base_type
from typing import Optional

@base_type
class Birthdate:
    '''
    Describes the birthdate of a user.
    '''

    month: int
    '''
    Month of the user's birth; 1-12
    '''

    day: int
    '''
    Day of the user's birth; 1-31
    '''

    year: Optional[int] = None
    '''
    Optional. Year of the user's birth
    '''

