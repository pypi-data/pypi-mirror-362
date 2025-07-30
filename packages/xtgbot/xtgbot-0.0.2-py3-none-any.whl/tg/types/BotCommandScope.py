from ..base_type import base_type
from typing import Optional

@base_type
class BotCommandScope:
    '''
    This object represents the scope to which bot commands are applied. Currently, the following 7 scopes are supported:
    - BotCommandScopeDefault
    - BotCommandScopeAllPrivateChats
    - BotCommandScopeAllGroupChats
    - BotCommandScopeAllChatAdministrators
    - BotCommandScopeChat
    - BotCommandScopeChatAdministrators
    - BotCommandScopeChatMember
    '''

    pass
