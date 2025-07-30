from .TransactionPartner import TransactionPartner
from ..base_type import base_type
from typing import Optional

@base_type
class TransactionPartnerOther(TransactionPartner):
    '''
    Describes a transaction with an unknown source or recipient.
    '''

    type: str
    '''
    Type of the transaction partner, always "other"
    '''

