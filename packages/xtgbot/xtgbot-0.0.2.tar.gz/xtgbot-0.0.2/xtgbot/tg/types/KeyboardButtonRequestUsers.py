from ..base_type import base_type
from typing import Optional

@base_type
class KeyboardButtonRequestUsers:
    '''
    This object defines the criteria used to request suitable users. Information about the selected users will be shared with the bot when the corresponding button is pressed. More about requesting users: https://core.telegram.org/bots/features#chat-and-user-selection
    '''

    request_id: int
    '''
    Signed 32-bit identifier of the request that will be received back in the UsersShared object. Must be unique within the message
    '''

    user_is_bot: bool = False
    '''
    Optional. Pass True to request bots, pass False to request regular users. If not specified, no additional restrictions are applied.
    '''

    user_is_premium: bool = False
    '''
    Optional. Pass True to request premium users, pass False to request non-premium users. If not specified, no additional restrictions are applied.
    '''

    max_quantity: Optional[int] = None
    '''
    Optional. The maximum number of users to be selected; 1-10. Defaults to 1.
    '''

    request_name: bool = False
    '''
    Optional. Pass True to request the users' first and last names
    '''

    request_username: bool = False
    '''
    Optional. Pass True to request the users' usernames
    '''

    request_photo: bool = False
    '''
    Optional. Pass True to request the users' photos
    '''

