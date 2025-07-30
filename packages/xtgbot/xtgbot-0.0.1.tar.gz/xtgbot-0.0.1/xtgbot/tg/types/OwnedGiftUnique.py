from .User import User
from .UniqueGift import UniqueGift
from .User import User
from .UniqueGift import UniqueGift
from .User import User
from .UniqueGift import UniqueGift
from .User import User
from .UniqueGift import UniqueGift
from .User import User
from .UniqueGift import UniqueGift
from .User import User
from .UniqueGift import UniqueGift
from .UniqueGift import UniqueGift
from .UniqueGift import UniqueGift
from .OwnedGift import OwnedGift
from ..base_type import base_type
from typing import Optional

@base_type
class OwnedGiftUnique(OwnedGift):
    '''
    Describes a unique gift received and owned by a user or a chat.
    '''

    send_date: int
    '''
    Date the gift was sent in Unix time
    '''

    gift: UniqueGift
    '''
    Information about the unique gift
    '''

    type: str
    '''
    Type of the gift, always "unique"
    '''

    owned_gift_id: Optional[str] = None
    '''
    Optional. Unique identifier of the received gift for the bot; for gifts received on behalf of business accounts only
    '''

    sender_user: Optional[User] = None
    '''
    Optional. Sender of the gift if it is a known user
    '''

    is_saved: bool = False
    '''
    Optional. True, if the gift is displayed on the account's profile page; for gifts received on behalf of business accounts only
    '''

    can_be_transferred: bool = False
    '''
    Optional. True, if the gift can be transferred to another owner; for gifts received on behalf of business accounts only
    '''

    transfer_star_count: Optional[int] = None
    '''
    Optional. Number of Telegram Stars that must be paid to transfer the gift; omitted if the bot cannot transfer the gift
    '''

    next_transfer_date: Optional[int] = None
    '''
    Optional. Point in time (Unix timestamp) when the gift can be transferred. If it is in the past, then the gift can be transferred now
    '''

