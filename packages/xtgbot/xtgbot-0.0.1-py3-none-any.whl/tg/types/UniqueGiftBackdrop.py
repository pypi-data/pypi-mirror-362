from .UniqueGiftBackdropColors import UniqueGiftBackdropColors
from .UniqueGiftBackdropColors import UniqueGiftBackdropColors
from ..base_type import base_type
from typing import Optional

@base_type
class UniqueGiftBackdrop:
    '''
    This object describes the backdrop of a unique gift.
    '''

    rarity_per_mille: int
    '''
    The number of unique gifts that receive this backdrop for every 1000 gifts upgraded
    '''

    colors: UniqueGiftBackdropColors
    '''
    Colors of the backdrop
    '''

    name: str
    '''
    Name of the backdrop
    '''

