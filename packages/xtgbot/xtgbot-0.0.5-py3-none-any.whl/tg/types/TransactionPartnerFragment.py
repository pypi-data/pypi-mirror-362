from .RevenueWithdrawalState import RevenueWithdrawalState
from .TransactionPartner import TransactionPartner
from ..base_type import base_type
from typing import Optional

@base_type
class TransactionPartnerFragment(TransactionPartner):
    '''
    Describes a withdrawal transaction with Fragment.
    '''

    type: str
    '''
    Type of the transaction partner, always "fragment"
    '''

    withdrawal_state: Optional[RevenueWithdrawalState] = None
    '''
    Optional. State of the transaction if the transaction is outgoing
    '''

