from .BackgroundFill import BackgroundFill
from ..base_type import base_type
from typing import Optional

@base_type
class BackgroundFillGradient(BackgroundFill):
    '''
    The background is a gradient fill.
    '''

    rotation_angle: int
    '''
    Clockwise rotation angle of the background fill in degrees; 0-359
    '''

    bottom_color: int
    '''
    Bottom color of the gradient in the RGB24 format
    '''

    top_color: int
    '''
    Top color of the gradient in the RGB24 format
    '''

    type: str
    '''
    Type of the background fill, always "gradient"
    '''

