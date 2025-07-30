from ..base_type import base_type
from typing import Optional

@base_type
class SwitchInlineQueryChosenChat:
    '''
    This object represents an inline button that switches the current user to inline mode in a chosen chat, with an optional default inline query.
    '''

    query: Optional[str] = None
    '''
    Optional. The default inline query to be inserted in the input field. If left empty, only the bot's username will be inserted
    '''

    allow_user_chats: bool = False
    '''
    Optional. True, if private chats with users can be chosen
    '''

    allow_bot_chats: bool = False
    '''
    Optional. True, if private chats with bots can be chosen
    '''

    allow_group_chats: bool = False
    '''
    Optional. True, if group and supergroup chats can be chosen
    '''

    allow_channel_chats: bool = False
    '''
    Optional. True, if channel chats can be chosen
    '''

