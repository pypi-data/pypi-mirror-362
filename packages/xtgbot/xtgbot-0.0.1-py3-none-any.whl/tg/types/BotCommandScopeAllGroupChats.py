from .BotCommandScope import BotCommandScope
from ..base_type import base_type
from typing import Optional

@base_type
class BotCommandScopeAllGroupChats(BotCommandScope):
    '''
    Represents the scope of bot commands, covering all group and supergroup chats.
    '''

    type: str
    '''
    Scope type, must be all_group_chats
    '''

