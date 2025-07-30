from .ReactionType import ReactionType
from .ReactionType import ReactionType
from .ReactionType import ReactionType
from .StoryAreaType import StoryAreaType
from ..base_type import base_type
from typing import Optional

@base_type
class StoryAreaTypeSuggestedReaction(StoryAreaType):
    '''
    Describes a story area pointing to a suggested reaction. Currently, a story can have up to 5 suggested reaction areas.
    '''

    reaction_type: ReactionType
    '''
    Type of the reaction
    '''

    type: str
    '''
    Type of the area, always "suggested_reaction"
    '''

    is_dark: bool = False
    '''
    Optional. Pass True if the reaction area has a dark background
    '''

    is_flipped: bool = False
    '''
    Optional. Pass True if reaction area corner is flipped
    '''

