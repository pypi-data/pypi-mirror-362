from .WebAppInfo import WebAppInfo
from .MenuButton import MenuButton
from ..base_type import base_type
from typing import Optional

@base_type
class MenuButtonWebApp(MenuButton):
    '''
    Represents a menu button, which launches a Web App.
    '''

    web_app: WebAppInfo
    '''
    Description of the Web App that will be launched when the user presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. Alternatively, a t.me link to a Web App of the bot can be specified in the object instead of the Web App's URL, in which case the Web App will be opened as if the user pressed the link.
    '''

    text: str
    '''
    Text on the button
    '''

    type: str
    '''
    Type of the button, must be web_app
    '''

