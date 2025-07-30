from ..base_type import base_type
from typing import Optional

@base_type
class BotCommand:
    '''
    This object represents a bot command.
    '''

    description: str
    '''
    Description of the command; 1-256 characters.
    '''

    command: str
    '''
    Text of the command; 1-32 characters. Can contain only lowercase English letters, digits and underscores.
    '''

