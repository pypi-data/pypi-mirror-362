from .BackgroundType import BackgroundType
from ..base_type import base_type
from typing import Optional

@base_type
class ChatBackground:
    '''
    This object represents a chat background.
    '''

    type: BackgroundType
    '''
    Type of the background
    '''

