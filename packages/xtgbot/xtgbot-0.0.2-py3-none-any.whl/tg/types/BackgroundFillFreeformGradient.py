from .BackgroundFill import BackgroundFill
from ..base_type import base_type
from typing import Optional

@base_type
class BackgroundFillFreeformGradient(BackgroundFill):
    '''
    The background is a freeform gradient that rotates after every message in the chat.
    '''

    colors: list[int]
    '''
    A list of the 3 or 4 base colors that are used to generate the freeform gradient in the RGB24 format
    '''

    type: str
    '''
    Type of the background fill, always "freeform_gradient"
    '''

