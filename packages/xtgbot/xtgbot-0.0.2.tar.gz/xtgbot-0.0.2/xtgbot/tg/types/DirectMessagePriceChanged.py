from ..base_type import base_type
from typing import Optional

@base_type
class DirectMessagePriceChanged:
    '''
    Describes a service message about a change in the price of direct messages sent to a channel chat.
    '''

    are_direct_messages_enabled: bool
    '''
    True, if direct messages are enabled for the channel chat; false otherwise
    '''

    direct_message_star_count: Optional[int] = None
    '''
    Optional. The new number of Telegram Stars that must be paid by users for each direct message sent to the channel. Does not apply to users who have been exempted by administrators. Defaults to 0.
    '''

