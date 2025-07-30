from .Sticker import Sticker
from .Sticker import Sticker
from ..base_type import base_type
from typing import Optional

@base_type
class UniqueGiftSymbol:
    '''
    This object describes the symbol shown on the pattern of a unique gift.
    '''

    rarity_per_mille: int
    '''
    The number of unique gifts that receive this model for every 1000 gifts upgraded
    '''

    sticker: Sticker
    '''
    The sticker that represents the unique gift
    '''

    name: str
    '''
    Name of the symbol
    '''

