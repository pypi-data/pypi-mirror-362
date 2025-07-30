from ..base_type import base_type
from typing import Optional

@base_type
class WebAppData:
    '''
    Describes data sent from a Web App to the bot.
    '''

    button_text: str
    '''
    Text of the web_app keyboard button from which the Web App was opened. Be aware that a bad client can send arbitrary data in this field.
    '''

    data: str
    '''
    The data. Be aware that a bad client can send arbitrary data in this field.
    '''

