from .ReactionType import ReactionType
from ..base_type import base_type
from typing import Optional

@base_type
class ReactionTypeCustomEmoji(ReactionType):
    '''
    The reaction is based on a custom emoji.
    '''

    custom_emoji_id: str
    '''
    Custom emoji identifier
    '''

    type: str
    '''
    Type of the reaction, always "custom_emoji"
    '''

