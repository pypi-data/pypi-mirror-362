from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class AffiliateInfo:
    '''
    Contains information about the affiliate that received a commission via this transaction.
    '''

    amount: int
    '''
    Integer amount of Telegram Stars received by the affiliate from the transaction, rounded to 0; can be negative for refunds
    '''

    commission_per_mille: int
    '''
    The number of Telegram Stars received by the affiliate for each 1000 Telegram Stars received by the bot from referred users
    '''

    affiliate_user: Optional[User] = None
    '''
    Optional. The bot or the user that received an affiliate commission if it was received by a bot or a user
    '''

    affiliate_chat: Optional[Chat] = None
    '''
    Optional. The chat that received an affiliate commission if it was received by a chat
    '''

    nanostar_amount: Optional[int] = None
    '''
    Optional. The number of 1/1000000000 shares of Telegram Stars received by the affiliate; from -999999999 to 999999999; can be negative for refunds
    '''

