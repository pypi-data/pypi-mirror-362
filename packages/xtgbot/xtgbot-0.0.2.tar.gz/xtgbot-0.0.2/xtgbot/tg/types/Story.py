from .Chat import Chat
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class Story:
    '''
    This object represents a story.
    '''

    id: int
    '''
    Unique identifier for the story in the chat
    '''

    chat: Chat
    '''
    Chat that posted the story
    '''

