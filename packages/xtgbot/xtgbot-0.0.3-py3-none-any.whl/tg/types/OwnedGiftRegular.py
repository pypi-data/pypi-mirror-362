from .User import User
from .Gift import Gift
from .MessageEntity import MessageEntity
from .User import User
from .Gift import Gift
from .MessageEntity import MessageEntity
from .User import User
from .Gift import Gift
from .MessageEntity import MessageEntity
from .User import User
from .Gift import Gift
from .MessageEntity import MessageEntity
from .User import User
from .Gift import Gift
from .MessageEntity import MessageEntity
from .User import User
from .Gift import Gift
from .MessageEntity import MessageEntity
from .User import User
from .Gift import Gift
from .MessageEntity import MessageEntity
from .User import User
from .Gift import Gift
from .User import User
from .Gift import Gift
from .User import User
from .Gift import Gift
from .Gift import Gift
from .Gift import Gift
from .OwnedGift import OwnedGift
from ..base_type import base_type
from typing import Optional

@base_type
class OwnedGiftRegular(OwnedGift):
    '''
    Describes a regular gift owned by a user or a chat.
    '''

    send_date: int
    '''
    Date the gift was sent in Unix time
    '''

    gift: Gift
    '''
    Information about the regular gift
    '''

    type: str
    '''
    Type of the gift, always "regular"
    '''

    owned_gift_id: Optional[str] = None
    '''
    Optional. Unique identifier of the gift for the bot; for gifts received on behalf of business accounts only
    '''

    sender_user: Optional[User] = None
    '''
    Optional. Sender of the gift if it is a known user
    '''

    text: Optional[str] = None
    '''
    Optional. Text of the message that was added to the gift
    '''

    entities: Optional[list[MessageEntity]] = None
    '''
    Optional. Special entities that appear in the text
    '''

    is_private: bool = False
    '''
    Optional. True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone will be able to see them
    '''

    is_saved: bool = False
    '''
    Optional. True, if the gift is displayed on the account's profile page; for gifts received on behalf of business accounts only
    '''

    can_be_upgraded: bool = False
    '''
    Optional. True, if the gift can be upgraded to a unique gift; for gifts received on behalf of business accounts only
    '''

    was_refunded: bool = False
    '''
    Optional. True, if the gift was refunded and isn't available anymore
    '''

    convert_star_count: Optional[int] = None
    '''
    Optional. Number of Telegram Stars that can be claimed by the receiver instead of the gift; omitted if the gift cannot be converted to Telegram Stars
    '''

    prepaid_upgrade_star_count: Optional[int] = None
    '''
    Optional. Number of Telegram Stars that were paid by the sender for the ability to upgrade the gift
    '''

