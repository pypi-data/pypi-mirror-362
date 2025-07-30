from .User import User
from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class ProximityAlertTriggered:
    '''
    This object represents the content of a service message, sent whenever a user in the chat triggers a proximity alert set by another user.
    '''

    distance: int
    '''
    The distance between the users
    '''

    watcher: User
    '''
    User that set the alert
    '''

    traveler: User
    '''
    User that triggered the alert
    '''

