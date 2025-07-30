from ..base_type import base_type
from typing import Optional

@base_type
class TransactionPartner:
    '''
    This object describes the source of a transaction, or its recipient for outgoing transactions. Currently, it can be one of
    - TransactionPartnerUser
    - TransactionPartnerChat
    - TransactionPartnerAffiliateProgram
    - TransactionPartnerFragment
    - TransactionPartnerTelegramAds
    - TransactionPartnerTelegramApi
    - TransactionPartnerOther
    '''

    pass
