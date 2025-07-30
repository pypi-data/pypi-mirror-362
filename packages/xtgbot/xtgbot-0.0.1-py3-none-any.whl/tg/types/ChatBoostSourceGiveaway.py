from .User import User
from .User import User
from .User import User
from .ChatBoostSource import ChatBoostSource
from ..base_type import base_type
from typing import Optional

@base_type
class ChatBoostSourceGiveaway(ChatBoostSource):
    '''
    The boost was obtained by the creation of a Telegram Premium or a Telegram Star giveaway. This boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription for Telegram Premium giveaways and prize_star_count / 500 times for one year for Telegram Star giveaways.
    '''

    giveaway_message_id: int
    '''
    Identifier of a message in the chat with the giveaway; the message could have been deleted already. May be 0 if the message isn't sent yet.
    '''

    source: str
    '''
    Source of the boost, always "giveaway"
    '''

    user: Optional[User] = None
    '''
    Optional. User that won the prize in the giveaway if any; for Telegram Premium giveaways only
    '''

    prize_star_count: Optional[int] = None
    '''
    Optional. The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only
    '''

    is_unclaimed: bool = False
    '''
    Optional. True, if the giveaway was completed, but there was no user to win the prize
    '''

