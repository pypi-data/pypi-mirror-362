from .MenuButton import MenuButton
from ..base_type import base_type
from typing import Optional

@base_type
class MenuButtonCommands(MenuButton):
    '''
    Represents a menu button, which opens the bot's list of commands.
    '''

    type: str
    '''
    Type of the button, must be commands
    '''

