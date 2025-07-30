from ..base_type import base_type
from typing import Optional

@base_type
class RefundedPayment:
    '''
    This object contains basic information about a refunded payment.
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
    Total refunded price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45, total_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
    '''

    currency: str
    '''
    Three-letter ISO 4217 currency code, or "XTR" for payments in Telegram Stars. Currently, always "XTR"
    '''

    provider_payment_charge_id: Optional[str] = None
    '''
    Optional. Provider payment identifier
    '''

