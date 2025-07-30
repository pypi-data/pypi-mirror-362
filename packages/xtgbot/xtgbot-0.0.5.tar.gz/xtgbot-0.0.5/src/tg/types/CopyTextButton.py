from ..base_type import base_type
from typing import Optional

@base_type
class CopyTextButton:
    '''
    This object represents an inline keyboard button that copies specified text to the clipboard.
    '''

    text: str
    '''
    The text to be copied to the clipboard; 1-256 characters
    '''

