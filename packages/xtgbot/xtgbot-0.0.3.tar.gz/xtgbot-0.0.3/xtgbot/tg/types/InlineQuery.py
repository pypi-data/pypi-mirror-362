from .User import User
from .Location import Location
from .User import User
from .User import User
from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class InlineQuery:
    '''
    This object represents an incoming inline query. When the user sends an empty query, your bot could return some default or trending results.
    '''

    offset: str
    '''
    Offset of the results to be returned, can be controlled by the bot
    '''

    query: str
    '''
    Text of the query (up to 256 characters)
    '''

    from_: User
    '''
    Sender
    '''

    id: str
    '''
    Unique identifier for this query
    '''

    chat_type: Optional[str] = None
    '''
    Optional. Type of the chat from which the inline query was sent. Can be either "sender" for a private chat with the inline query sender, "private", "group", "supergroup", or "channel". The chat type should be always known for requests sent from official clients and most third-party clients, unless the request was sent from a secret chat
    '''

    location: Optional[Location] = None
    '''
    Optional. Sender location, only for bots that request user location
    '''

