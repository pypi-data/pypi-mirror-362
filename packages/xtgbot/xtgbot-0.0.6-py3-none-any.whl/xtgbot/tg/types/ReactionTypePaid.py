from .ReactionType import ReactionType
from ..base_type import base_type
from typing import Optional

@base_type
class ReactionTypePaid(ReactionType):
    '''
    The reaction is paid.
    '''

    type: str
    '''
    Type of the reaction, always "paid"
    '''

