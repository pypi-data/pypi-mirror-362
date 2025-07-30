from .InlineKeyboardButton import InlineKeyboardButton
from ..base_type import base_type
from typing import Optional

@base_type
class InlineKeyboardMarkup:
    '''
    This object represents an inline keyboard that appears right next to the message it belongs to.
    '''

    inline_keyboard: list[list[InlineKeyboardButton]]
    '''
    Array of button rows, each represented by an Array of InlineKeyboardButton objects
    '''

