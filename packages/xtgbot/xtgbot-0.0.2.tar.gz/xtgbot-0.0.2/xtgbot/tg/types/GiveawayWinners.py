from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class GiveawayWinners:
    '''
    This object represents a message about the completion of a giveaway with public winners.
    '''

    winners: list[User]
    '''
    List of up to 100 winners of the giveaway
    '''

    winner_count: int
    '''
    Total number of winners in the giveaway
    '''

    winners_selection_date: int
    '''
    Point in time (Unix timestamp) when winners of the giveaway were selected
    '''

    giveaway_message_id: int
    '''
    Identifier of the message with the giveaway in the chat
    '''

    chat: Chat
    '''
    The chat that created the giveaway
    '''

    additional_chat_count: Optional[int] = None
    '''
    Optional. The number of other chats the user had to join in order to be eligible for the giveaway
    '''

    prize_star_count: Optional[int] = None
    '''
    Optional. The number of Telegram Stars that were split between giveaway winners; for Telegram Star giveaways only
    '''

    premium_subscription_month_count: Optional[int] = None
    '''
    Optional. The number of months the Telegram Premium subscription won from the giveaway will be active for; for Telegram Premium giveaways only
    '''

    unclaimed_prize_count: Optional[int] = None
    '''
    Optional. Number of undistributed prizes
    '''

    only_new_members: bool = False
    '''
    Optional. True, if only users who had joined the chats after the giveaway started were eligible to win
    '''

    was_refunded: bool = False
    '''
    Optional. True, if the giveaway was canceled because the payment for it was refunded
    '''

    prize_description: Optional[str] = None
    '''
    Optional. Description of additional giveaway prize
    '''

