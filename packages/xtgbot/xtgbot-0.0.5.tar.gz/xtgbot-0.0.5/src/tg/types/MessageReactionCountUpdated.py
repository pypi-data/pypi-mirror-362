from .Chat import Chat
from .ReactionCount import ReactionCount
from .Chat import Chat
from .Chat import Chat
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class MessageReactionCountUpdated:
    '''
    This object represents reaction changes on a message with anonymous reactions.
    '''

    reactions: list[ReactionCount]
    '''
    List of reactions that are present on the message
    '''

    date: int
    '''
    Date of the change in Unix time
    '''

    message_id: int
    '''
    Unique message identifier inside the chat
    '''

    chat: Chat
    '''
    The chat containing the message
    '''

