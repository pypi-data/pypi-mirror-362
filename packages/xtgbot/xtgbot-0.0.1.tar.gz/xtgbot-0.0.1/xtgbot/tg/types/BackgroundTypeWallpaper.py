from .Document import Document
from .Document import Document
from .Document import Document
from .Document import Document
from .BackgroundType import BackgroundType
from ..base_type import base_type
from typing import Optional

@base_type
class BackgroundTypeWallpaper(BackgroundType):
    '''
    The background is a wallpaper in the JPEG format.
    '''

    dark_theme_dimming: int
    '''
    Dimming of the background in dark themes, as a percentage; 0-100
    '''

    document: Document
    '''
    Document with the wallpaper
    '''

    type: str
    '''
    Type of the background, always "wallpaper"
    '''

    is_blurred: bool = False
    '''
    Optional. True, if the wallpaper is downscaled to fit in a 450x450 square and then box-blurred with radius 12
    '''

    is_moving: bool = False
    '''
    Optional. True, if the background moves slightly when the device is tilted
    '''

