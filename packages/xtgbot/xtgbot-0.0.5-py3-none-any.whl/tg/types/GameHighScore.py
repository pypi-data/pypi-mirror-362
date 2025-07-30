from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class GameHighScore:
    '''
    This object represents one row of the high scores table for a game.
    '''

    score: int
    '''
    Score
    '''

    user: User
    '''
    User
    '''

    position: int
    '''
    Position in high score table for the game
    '''

