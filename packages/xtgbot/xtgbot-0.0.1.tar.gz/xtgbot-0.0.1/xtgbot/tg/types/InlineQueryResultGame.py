from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InlineQueryResult import InlineQueryResult
from ..base_type import base_type
from typing import Optional

@base_type
class InlineQueryResultGame(InlineQueryResult):
    '''
    Represents a Game.
    '''

    game_short_name: str
    '''
    Short name of the game
    '''

    id: str
    '''
    Unique identifier for this result, 1-64 bytes
    '''

    type: str
    '''
    Type of the result, must be game
    '''

    reply_markup: Optional[InlineKeyboardMarkup] = None
    '''
    Optional. Inline keyboard attached to the message
    '''

