from .BotCommandScope import BotCommandScope
from ..base_type import base_type
from typing import Optional

@base_type
class BotCommandScopeDefault(BotCommandScope):
    '''
    Represents the default scope of bot commands. Default commands are used if no commands with a narrower scope are specified for the user.
    '''

    type: str
    '''
    Scope type, must be default
    '''

