from ..base_type import base_type
from typing import Optional

@base_type
class KeyboardButtonPollType:
    '''
    This object represents type of a poll, which is allowed to be created and sent when the corresponding button is pressed.
    '''

    type: Optional[str] = None
    '''
    Optional. If quiz is passed, the user will be allowed to create only polls in the quiz mode. If regular is passed, only regular polls will be allowed. Otherwise, the user will be allowed to create a poll of any type.
    '''

