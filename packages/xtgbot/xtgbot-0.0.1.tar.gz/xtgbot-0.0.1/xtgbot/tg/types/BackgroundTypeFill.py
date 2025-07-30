from .BackgroundFill import BackgroundFill
from .BackgroundFill import BackgroundFill
from .BackgroundType import BackgroundType
from ..base_type import base_type
from typing import Optional

@base_type
class BackgroundTypeFill(BackgroundType):
    '''
    The background is automatically filled based on the selected colors.
    '''

    dark_theme_dimming: int
    '''
    Dimming of the background in dark themes, as a percentage; 0-100
    '''

    fill: BackgroundFill
    '''
    The background fill
    '''

    type: str
    '''
    Type of the background, always "fill"
    '''

