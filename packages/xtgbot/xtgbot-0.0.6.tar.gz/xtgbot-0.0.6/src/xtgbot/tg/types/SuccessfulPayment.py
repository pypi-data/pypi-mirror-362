from .OrderInfo import OrderInfo
from .OrderInfo import OrderInfo
from .OrderInfo import OrderInfo
from ..base_type import base_type
from typing import Optional

@base_type
class SuccessfulPayment:
    '''
    This object contains basic information about a successful payment. Note that if the buyer initiates a chargeback with the relevant payment provider following this transaction, the funds may be debited from your balance. This is outside of Telegram's control.
    '''

    provider_payment_charge_id: str
    '''
    Provider payment identifier
    '''

    telegram_payment_charge_id: str
    '''
    Telegram payment identifier
    '''

    invoice_payload: str
    '''
    Bot-specified invoice payload
    '''

    total_amount: int
    '''
    Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
    '''

    currency: str
    '''
    Three-letter ISO 4217 currency code, or "XTR" for payments in Telegram Stars
    '''

    subscription_expiration_date: Optional[int] = None
    '''
    Optional. Expiration date of the subscription, in Unix time; for recurring payments only
    '''

    is_recurring: bool = False
    '''
    Optional. True, if the payment is a recurring payment for a subscription
    '''

    is_first_recurring: bool = False
    '''
    Optional. True, if the payment is the first payment for a subscription
    '''

    shipping_option_id: Optional[str] = None
    '''
    Optional. Identifier of the shipping option chosen by the user
    '''

    order_info: Optional[OrderInfo] = None
    '''
    Optional. Order information provided by the user
    '''

