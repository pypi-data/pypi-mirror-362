from .User import User
from .OrderInfo import OrderInfo
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class PreCheckoutQuery:
    '''
    This object contains information about an incoming pre-checkout query.
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

    from_: User
    '''
    User who sent the query
    '''

    id: str
    '''
    Unique query identifier
    '''

    shipping_option_id: Optional[str] = None
    '''
    Optional. Identifier of the shipping option chosen by the user
    '''

    order_info: Optional[OrderInfo] = None
    '''
    Optional. Order information provided by the user
    '''

