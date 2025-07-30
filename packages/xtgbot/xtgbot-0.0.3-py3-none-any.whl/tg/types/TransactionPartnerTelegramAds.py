from .TransactionPartner import TransactionPartner
from ..base_type import base_type
from typing import Optional

@base_type
class TransactionPartnerTelegramAds(TransactionPartner):
    '''
    Describes a withdrawal transaction to the Telegram Ads platform.
    '''

    type: str
    '''
    Type of the transaction partner, always "telegram_ads"
    '''

