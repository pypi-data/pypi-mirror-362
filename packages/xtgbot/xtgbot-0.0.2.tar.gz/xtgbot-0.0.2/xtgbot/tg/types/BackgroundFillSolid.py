from .BackgroundFill import BackgroundFill
from ..base_type import base_type
from typing import Optional

@base_type
class BackgroundFillSolid(BackgroundFill):
    '''
    The background is filled using the selected color.
    '''

    color: int
    '''
    The color of the background fill in the RGB24 format
    '''

    type: str
    '''
    Type of the background fill, always "solid"
    '''

