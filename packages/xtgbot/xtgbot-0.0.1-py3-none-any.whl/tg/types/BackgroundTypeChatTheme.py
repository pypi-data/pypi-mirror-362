from .BackgroundType import BackgroundType
from ..base_type import base_type
from typing import Optional

@base_type
class BackgroundTypeChatTheme(BackgroundType):
    '''
    The background is taken directly from a built-in chat theme.
    '''

    theme_name: str
    '''
    Name of the chat theme, which is usually an emoji
    '''

    type: str
    '''
    Type of the background, always "chat_theme"
    '''

