from .User import User
from .Location import Location
from .User import User
from .Location import Location
from .User import User
from .Location import Location
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class ChosenInlineResult:
    '''
    Represents a result of an inline query that was chosen by the user and sent to their chat partner.
    Note: It is necessary to enable inline feedback via @BotFather in order to receive these objects in updates.
    '''

    query: str
    '''
    The query that was used to obtain the result
    '''

    from_: User
    '''
    The user that chose the result
    '''

    result_id: str
    '''
    The unique identifier for the result that was chosen
    '''

    location: Optional[Location] = None
    '''
    Optional. Sender location, only for bots that require user location
    '''

    inline_message_id: Optional[str] = None
    '''
    Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached to the message. Will be also received in callback queries and can be used to edit the message.
    '''

