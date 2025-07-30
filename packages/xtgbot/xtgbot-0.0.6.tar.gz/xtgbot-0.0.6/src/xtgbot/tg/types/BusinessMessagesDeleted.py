from .Chat import Chat
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class BusinessMessagesDeleted:
    '''
    This object is received when messages are deleted from a connected business account.
    '''

    message_ids: list[int]
    '''
    The list of identifiers of deleted messages in the chat of the business account
    '''

    chat: Chat
    '''
    Information about a chat in the business account. The bot may not have access to the chat or the corresponding user.
    '''

    business_connection_id: str
    '''
    Unique identifier of the business connection
    '''

