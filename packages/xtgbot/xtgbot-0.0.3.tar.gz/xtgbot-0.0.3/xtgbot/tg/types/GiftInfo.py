from .Gift import Gift
from .MessageEntity import MessageEntity
from .Gift import Gift
from .MessageEntity import MessageEntity
from .Gift import Gift
from .Gift import Gift
from .Gift import Gift
from .Gift import Gift
from .Gift import Gift
from .Gift import Gift
from ..base_type import base_type
from typing import Optional

@base_type
class GiftInfo:
    '''
    Describes a service message about a regular gift that was sent or received.
    '''

    gift: Gift
    '''
    Information about the gift
    '''

    owned_gift_id: Optional[str] = None
    '''
    Optional. Unique identifier of the received gift for the bot; only present for gifts received on behalf of business accounts
    '''

    convert_star_count: Optional[int] = None
    '''
    Optional. Number of Telegram Stars that can be claimed by the receiver by converting the gift; omitted if conversion to Telegram Stars is impossible
    '''

    prepaid_upgrade_star_count: Optional[int] = None
    '''
    Optional. Number of Telegram Stars that were prepaid by the sender for the ability to upgrade the gift
    '''

    can_be_upgraded: bool = False
    '''
    Optional. True, if the gift can be upgraded to a unique gift
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

