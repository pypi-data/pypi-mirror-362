from .BackgroundFill import BackgroundFill
from .Document import Document
from .BackgroundFill import BackgroundFill
from .Document import Document
from .BackgroundFill import BackgroundFill
from .Document import Document
from .BackgroundFill import BackgroundFill
from .Document import Document
from .Document import Document
from .BackgroundType import BackgroundType
from ..base_type import base_type
from typing import Optional

@base_type
class BackgroundTypePattern(BackgroundType):
    '''
    The background is a .PNG or .TGV (gzipped subset of SVG with MIME type "application/x-tgwallpattern") pattern to be combined with the background fill chosen by the user.
    '''

    intensity: int
    '''
    Intensity of the pattern when it is shown above the filled background; 0-100
    '''

    fill: BackgroundFill
    '''
    The background fill that is combined with the pattern
    '''

    document: Document
    '''
    Document with the pattern
    '''

    type: str
    '''
    Type of the background, always "pattern"
    '''

    is_inverted: bool = False
    '''
    Optional. True, if the background fill must be applied only to the pattern itself. All other pixels are black in this case. For dark themes only
    '''

    is_moving: bool = False
    '''
    Optional. True, if the background moves slightly when the device is tilted
    '''

