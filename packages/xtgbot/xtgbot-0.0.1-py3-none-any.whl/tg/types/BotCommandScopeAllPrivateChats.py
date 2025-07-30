from .BotCommandScope import BotCommandScope
from ..base_type import base_type
from typing import Optional

@base_type
class BotCommandScopeAllPrivateChats(BotCommandScope):
    '''
    Represents the scope of bot commands, covering all private chats.
    '''

    type: str
    '''
    Scope type, must be all_private_chats
    '''

