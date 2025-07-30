from .TransactionPartner import TransactionPartner
from .TransactionPartner import TransactionPartner
from ..base_type import base_type
from typing import Optional

@base_type
class StarTransaction:
    '''
    Describes a Telegram Star transaction. Note that if the buyer initiates a chargeback with the payment provider from whom they acquired Stars (e.g., Apple, Google) following this transaction, the refunded Stars will be deducted from the bot's balance. This is outside of Telegram's control.
    '''

    date: int
    '''
    Date the transaction was created in Unix time
    '''

    amount: int
    '''
    Integer amount of Telegram Stars transferred by the transaction
    '''

    id: str
    '''
    Unique identifier of the transaction. Coincides with the identifier of the original transaction for refund transactions. Coincides with SuccessfulPayment.telegram_payment_charge_id for successful incoming payments from users.
    '''

    nanostar_amount: Optional[int] = None
    '''
    Optional. The number of 1/1000000000 shares of Telegram Stars transferred by the transaction; from 0 to 999999999
    '''

    source: Optional[TransactionPartner] = None
    '''
    Optional. Source of an incoming transaction (e.g., a user purchasing goods or services, Fragment refunding a failed withdrawal). Only for incoming transactions
    '''

    receiver: Optional[TransactionPartner] = None
    '''
    Optional. Receiver of an outgoing transaction (e.g., a user for a purchase refund, Fragment for a withdrawal). Only for outgoing transactions
    '''

