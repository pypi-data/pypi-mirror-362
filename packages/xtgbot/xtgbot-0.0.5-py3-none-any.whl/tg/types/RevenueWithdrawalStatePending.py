from .RevenueWithdrawalState import RevenueWithdrawalState
from ..base_type import base_type
from typing import Optional

@base_type
class RevenueWithdrawalStatePending(RevenueWithdrawalState):
    '''
    The withdrawal is in progress.
    '''

    type: str
    '''
    Type of the state, always "pending"
    '''

