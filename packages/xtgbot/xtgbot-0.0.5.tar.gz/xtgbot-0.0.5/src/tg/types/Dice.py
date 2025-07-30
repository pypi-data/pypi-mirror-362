from ..base_type import base_type
from typing import Optional

@base_type
class Dice:
    '''
    This object represents an animated emoji that displays a random value.
    '''

    value: int
    '''
    Value of the dice, 1-6 for "🎲", "🎯" and "🎳" base emoji, 1-5 for "🏀" and "⚽" base emoji, 1-64 for "🎰" base emoji
    '''

    emoji: str
    '''
    Emoji on which the dice throw animation is based
    '''

