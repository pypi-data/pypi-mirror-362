from ..base_type import base_type
from typing import Optional

@base_type
class UniqueGiftBackdropColors:
    '''
    This object describes the colors of the backdrop of a unique gift.
    '''

    text_color: int
    '''
    The color for the text on the backdrop in RGB format
    '''

    symbol_color: int
    '''
    The color to be applied to the symbol in RGB format
    '''

    edge_color: int
    '''
    The color on the edges of the backdrop in RGB format
    '''

    center_color: int
    '''
    The color in the center of the backdrop in RGB format
    '''

