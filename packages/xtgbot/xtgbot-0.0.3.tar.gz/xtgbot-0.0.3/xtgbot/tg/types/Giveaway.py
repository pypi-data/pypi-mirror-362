from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class Giveaway:
    '''
    This object represents a message about a scheduled giveaway.
    '''

    winner_count: int
    '''
    The number of users which are supposed to be selected as winners of the giveaway
    '''

    winners_selection_date: int
    '''
    Point in time (Unix timestamp) when winners of the giveaway will be selected
    '''

    chats: list[Chat]
    '''
    The list of chats which the user must join to participate in the giveaway
    '''

    only_new_members: bool = False
    '''
    Optional. True, if only users who join the chats after the giveaway started should be eligible to win
    '''

    has_public_winners: bool = False
    '''
    Optional. True, if the list of giveaway winners will be visible to everyone
    '''

    prize_description: Optional[str] = None
    '''
    Optional. Description of additional giveaway prize
    '''

    country_codes: Optional[list[str]] = None
    '''
    Optional. A list of two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which eligible users for the giveaway must come. If empty, then all users can participate in the giveaway. Users with a phone number that was bought on Fragment can always participate in giveaways.
    '''

    prize_star_count: Optional[int] = None
    '''
    Optional. The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only
    '''

    premium_subscription_month_count: Optional[int] = None
    '''
    Optional. The number of months the Telegram Premium subscription won from the giveaway will be active for; for Telegram Premium giveaways only
    '''

