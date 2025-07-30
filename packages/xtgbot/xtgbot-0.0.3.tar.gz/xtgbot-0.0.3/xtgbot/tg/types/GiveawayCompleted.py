# from .Message import Message
# from .Message import Message
from ..base_type import base_type
from typing import Optional

@base_type
class GiveawayCompleted:
    '''
    This object represents a service message about the completion of a giveaway without public winners.
    '''

  # avoid circular import
  # avoid circular import
    winner_count: int
    '''
    Number of winners in the giveaway
    '''

    unclaimed_prize_count: Optional[int] = None
    '''
    Optional. Number of undistributed prizes
    '''

    giveaway_message: Optional['Message'] = None
    '''
    Optional. Message with the giveaway that was completed, if it wasn't deleted
    '''

    is_star_giveaway: bool = False
    '''
    Optional. True, if the giveaway is a Telegram Star giveaway. Otherwise, currently, the giveaway is a Telegram Premium giveaway.
    '''

