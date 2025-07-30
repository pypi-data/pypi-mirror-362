from .UniqueGiftBackdrop import UniqueGiftBackdrop
from .UniqueGiftSymbol import UniqueGiftSymbol
from .UniqueGiftModel import UniqueGiftModel
from .UniqueGiftSymbol import UniqueGiftSymbol
from .UniqueGiftModel import UniqueGiftModel
from .UniqueGiftModel import UniqueGiftModel
from ..base_type import base_type
from typing import Optional

@base_type
class UniqueGift:
    '''
    This object describes a unique gift that was upgraded from a regular gift.
    '''

    backdrop: UniqueGiftBackdrop
    '''
    Backdrop of the gift
    '''

    symbol: UniqueGiftSymbol
    '''
    Symbol of the gift
    '''

    model: UniqueGiftModel
    '''
    Model of the gift
    '''

    number: int
    '''
    Unique number of the upgraded gift among gifts upgraded from the same regular gift
    '''

    name: str
    '''
    Unique name of the gift. This name can be used in https://t.me/nft/... links and story areas
    '''

    base_name: str
    '''
    Human-readable name of the regular gift from which this unique gift was upgraded
    '''

