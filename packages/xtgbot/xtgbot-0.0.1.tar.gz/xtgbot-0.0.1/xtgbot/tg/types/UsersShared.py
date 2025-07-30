from .SharedUser import SharedUser
from ..base_type import base_type
from typing import Optional

@base_type
class UsersShared:
    '''
    This object contains information about the users whose identifiers were shared with the bot using a KeyboardButtonRequestUsers button.
    '''

    users: list[SharedUser]
    '''
    Information about users shared with the bot.
    '''

    request_id: int
    '''
    Identifier of the request
    '''

