from .ReactionType import ReactionType
from .Chat import Chat
from .User import User
from .ReactionType import ReactionType
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class MessageReactionUpdated:
    '''
    This object represents a change of a reaction on a message performed by a user.
    '''

    new_reaction: list[ReactionType]
    '''
    New list of reaction types that have been set by the user
    '''

    old_reaction: list[ReactionType]
    '''
    Previous list of reaction types that were set by the user
    '''

    date: int
    '''
    Date of the change in Unix time
    '''

    message_id: int
    '''
    Unique identifier of the message inside the chat
    '''

    chat: Chat
    '''
    The chat containing the message the user reacted to
    '''

    user: Optional[User] = None
    '''
    Optional. The user that changed the reaction, if the user isn't anonymous
    '''

    actor_chat: Optional[Chat] = None
    '''
    Optional. The chat on behalf of which the reaction was changed, if the user is anonymous
    '''

