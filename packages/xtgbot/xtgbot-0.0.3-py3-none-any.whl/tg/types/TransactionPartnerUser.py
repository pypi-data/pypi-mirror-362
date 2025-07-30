from .PaidMedia import PaidMedia
from .User import User
from .AffiliateInfo import AffiliateInfo
from .Gift import Gift
from .PaidMedia import PaidMedia
from .User import User
from .AffiliateInfo import AffiliateInfo
from .Gift import Gift
from .PaidMedia import PaidMedia
from .User import User
from .AffiliateInfo import AffiliateInfo
from .PaidMedia import PaidMedia
from .User import User
from .AffiliateInfo import AffiliateInfo
from .User import User
from .AffiliateInfo import AffiliateInfo
from .User import User
from .AffiliateInfo import AffiliateInfo
from .User import User
from .AffiliateInfo import AffiliateInfo
from .User import User
from .TransactionPartner import TransactionPartner
from ..base_type import base_type
from typing import Optional

@base_type
class TransactionPartnerUser(TransactionPartner):
    '''
    Describes a transaction with a user.
    '''

    user: User
    '''
    Information about the user
    '''

    transaction_type: str
    '''
    Type of the transaction, currently one of "invoice_payment" for payments via invoices, "paid_media_payment" for payments for paid media, "gift_purchase" for gifts sent by the bot, "premium_purchase" for Telegram Premium subscriptions gifted by the bot, "business_account_transfer" for direct transfers from managed business accounts
    '''

    type: str
    '''
    Type of the transaction partner, always "user"
    '''

    affiliate: Optional[AffiliateInfo] = None
    '''
    Optional. Information about the affiliate that received a commission via this transaction. Can be available only for "invoice_payment" and "paid_media_payment" transactions.
    '''

    invoice_payload: Optional[str] = None
    '''
    Optional. Bot-specified invoice payload. Can be available only for "invoice_payment" transactions.
    '''

    subscription_period: Optional[int] = None
    '''
    Optional. The duration of the paid subscription. Can be available only for "invoice_payment" transactions.
    '''

    paid_media: Optional[list[PaidMedia]] = None
    '''
    Optional. Information about the paid media bought by the user; for "paid_media_payment" transactions only
    '''

    paid_media_payload: Optional[str] = None
    '''
    Optional. Bot-specified paid media payload. Can be available only for "paid_media_payment" transactions.
    '''

    gift: Optional[Gift] = None
    '''
    Optional. The gift sent to the user by the bot; for "gift_purchase" transactions only
    '''

    premium_subscription_duration: Optional[int] = None
    '''
    Optional. Number of months the gifted Telegram Premium subscription will be active for; for "premium_purchase" transactions only
    '''

