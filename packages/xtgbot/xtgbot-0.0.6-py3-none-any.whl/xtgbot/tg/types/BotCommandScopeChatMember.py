from .BotCommandScope import BotCommandScope
from ..base_type import base_type
from typing import Optional

@base_type
class BotCommandScopeChatMember(BotCommandScope):
    '''
    Represents the scope of bot commands, covering a specific member of a group or supergroup chat.
    '''

    user_id: int
    '''
    Unique identifier of the target user
    '''

    chat_id: int |str
    '''
    Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    '''

    type: str
    '''
    Scope type, must be chat_member
    '''

