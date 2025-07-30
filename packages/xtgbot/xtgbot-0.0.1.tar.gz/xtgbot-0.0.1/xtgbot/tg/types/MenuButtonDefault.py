from .MenuButton import MenuButton
from ..base_type import base_type
from typing import Optional

@base_type
class MenuButtonDefault(MenuButton):
    '''
    Describes that no specific value for the menu button was set.
    '''

    type: str
    '''
    Type of the button, must be default
    '''

