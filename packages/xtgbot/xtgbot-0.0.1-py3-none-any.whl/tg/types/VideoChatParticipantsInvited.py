from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class VideoChatParticipantsInvited:
    '''
    This object represents a service message about new members invited to a video chat.
    '''

    users: list[User]
    '''
    New members that were invited to the video chat
    '''

