from ..base_type import base_type
from typing import Optional

@base_type
class GiveawayCreated:
    '''
    This object represents a service message about the creation of a scheduled giveaway.
    '''

    prize_star_count: Optional[int] = None
    '''
    Optional. The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only
    '''

