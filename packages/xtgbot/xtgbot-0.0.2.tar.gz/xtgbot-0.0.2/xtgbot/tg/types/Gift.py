from .Sticker import Sticker
from .Sticker import Sticker
from .Sticker import Sticker
from .Sticker import Sticker
from .Sticker import Sticker
from ..base_type import base_type
from typing import Optional

@base_type
class Gift:
    '''
    This object represents a gift that can be sent by the bot.
    '''

    star_count: int
    '''
    The number of Telegram Stars that must be paid to send the sticker
    '''

    sticker: Sticker
    '''
    The sticker that represents the gift
    '''

    id: str
    '''
    Unique identifier of the gift
    '''

    upgrade_star_count: Optional[int] = None
    '''
    Optional. The number of Telegram Stars that must be paid to upgrade the gift to a unique one
    '''

    total_count: Optional[int] = None
    '''
    Optional. The total number of the gifts of this type that can be sent; for limited gifts only
    '''

    remaining_count: Optional[int] = None
    '''
    Optional. The number of remaining gifts of this type that can be sent; for limited gifts only
    '''

