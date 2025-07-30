from .User import User
from .User import User
from .TransactionPartner import TransactionPartner
from ..base_type import base_type
from typing import Optional

@base_type
class TransactionPartnerAffiliateProgram(TransactionPartner):
    '''
    Describes the affiliate program that issued the affiliate commission received via this transaction.
    '''

    commission_per_mille: int
    '''
    The number of Telegram Stars received by the bot for each 1000 Telegram Stars received by the affiliate program sponsor from referred users
    '''

    type: str
    '''
    Type of the transaction partner, always "affiliate_program"
    '''

    sponsor_user: Optional[User] = None
    '''
    Optional. Information about the bot that sponsored the affiliate program
    '''

