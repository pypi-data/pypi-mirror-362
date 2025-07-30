from .PhotoSize import PhotoSize
from ..base_type import base_type
from typing import Optional

@base_type
class ChatShared:
    '''
    This object contains information about a chat that was shared with the bot using a KeyboardButtonRequestChat button.
    '''

    chat_id: int
    '''
    Identifier of the shared chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier. The bot may not have access to the chat and could be unable to use this identifier, unless the chat is already known to the bot by some other means.
    '''

    request_id: int
    '''
    Identifier of the request
    '''

    title: Optional[str] = None
    '''
    Optional. Title of the chat, if the title was requested by the bot.
    '''

    username: Optional[str] = None
    '''
    Optional. Username of the chat, if the username was requested by the bot and available.
    '''

    photo: Optional[list[PhotoSize]] = None
    '''
    Optional. Available sizes of the chat photo, if the photo was requested by the bot
    '''

