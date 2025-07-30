from .BotCommandScope import BotCommandScope
from ..base_type import base_type
from typing import Optional

@base_type
class BotCommandScopeAllChatAdministrators(BotCommandScope):
    '''
    Represents the scope of bot commands, covering all group and supergroup chat administrators.
    '''

    type: str
    '''
    Scope type, must be all_chat_administrators
    '''

