from .StarTransaction import StarTransaction
from ..base_type import base_type
from typing import Optional

@base_type
class StarTransactions:
    '''
    Contains a list of Telegram Star transactions.
    '''

    transactions: list[StarTransaction]
    '''
    The list of transactions
    '''

