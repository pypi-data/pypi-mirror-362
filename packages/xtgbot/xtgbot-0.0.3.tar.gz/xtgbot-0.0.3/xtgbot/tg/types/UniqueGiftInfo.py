from .UniqueGift import UniqueGift
from .UniqueGift import UniqueGift
from .UniqueGift import UniqueGift
from .UniqueGift import UniqueGift
from .UniqueGift import UniqueGift
from .UniqueGift import UniqueGift
from ..base_type import base_type
from typing import Optional

@base_type
class UniqueGiftInfo:
    '''
    Describes a service message about a unique gift that was sent or received.
    '''

    origin: str
    '''
    Origin of the gift. Currently, either "upgrade" for gifts upgraded from regular gifts, "transfer" for gifts transferred from other users or channels, or "resale" for gifts bought from other users
    '''

    gift: UniqueGift
    '''
    Information about the gift
    '''

    last_resale_star_count: Optional[int] = None
    '''
    Optional. For gifts bought from other users, the price paid for the gift
    '''

    owned_gift_id: Optional[str] = None
    '''
    Optional. Unique identifier of the received gift for the bot; only present for gifts received on behalf of business accounts
    '''

    transfer_star_count: Optional[int] = None
    '''
    Optional. Number of Telegram Stars that must be paid to transfer the gift; omitted if the bot cannot transfer the gift
    '''

    next_transfer_date: Optional[int] = None
    '''
    Optional. Point in time (Unix timestamp) when the gift can be transferred. If it is in the past, then the gift can be transferred now
    '''

