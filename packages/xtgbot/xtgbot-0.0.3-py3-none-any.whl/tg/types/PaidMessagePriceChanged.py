from ..base_type import base_type
from typing import Optional

@base_type
class PaidMessagePriceChanged:
    '''
    Describes a service message about a change in the price of paid messages within a chat.
    '''

    paid_message_star_count: int
    '''
    The new number of Telegram Stars that must be paid by non-administrator users of the supergroup chat for each sent message
    '''

