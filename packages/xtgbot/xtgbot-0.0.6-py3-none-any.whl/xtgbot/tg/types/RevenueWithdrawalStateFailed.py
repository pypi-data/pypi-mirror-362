from .RevenueWithdrawalState import RevenueWithdrawalState
from ..base_type import base_type
from typing import Optional

@base_type
class RevenueWithdrawalStateFailed(RevenueWithdrawalState):
    '''
    The withdrawal failed and the transaction was refunded.
    '''

    type: str
    '''
    Type of the state, always "failed"
    '''

