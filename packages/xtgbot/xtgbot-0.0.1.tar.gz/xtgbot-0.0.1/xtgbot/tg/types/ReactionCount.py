from .ReactionType import ReactionType
from .ReactionType import ReactionType
from ..base_type import base_type
from typing import Optional

@base_type
class ReactionCount:
    '''
    Represents a reaction added to a message along with the number of times it was added.
    '''

    total_count: int
    '''
    Number of times the reaction was added
    '''

    type: ReactionType
    '''
    Type of the reaction
    '''

