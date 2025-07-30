from .TransactionPartner import TransactionPartner
from ..base_type import base_type
from typing import Optional

@base_type
class TransactionPartnerTelegramApi(TransactionPartner):
    '''
    Describes a transaction with payment for paid broadcasting.
    '''

    request_count: int
    '''
    The number of successful requests that exceeded regular limits and were therefore billed
    '''

    type: str
    '''
    Type of the transaction partner, always "telegram_api"
    '''

