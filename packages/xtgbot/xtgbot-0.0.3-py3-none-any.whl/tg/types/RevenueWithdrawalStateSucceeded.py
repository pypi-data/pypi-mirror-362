from .RevenueWithdrawalState import RevenueWithdrawalState
from ..base_type import base_type
from typing import Optional

@base_type
class RevenueWithdrawalStateSucceeded(RevenueWithdrawalState):
    '''
    The withdrawal succeeded.
    '''

    url: str
    '''
    An HTTPS URL that can be used to see transaction details
    '''

    date: int
    '''
    Date the withdrawal was completed in Unix time
    '''

    type: str
    '''
    Type of the state, always "succeeded"
    '''

