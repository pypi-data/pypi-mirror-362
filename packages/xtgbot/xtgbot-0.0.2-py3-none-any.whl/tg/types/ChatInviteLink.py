from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from ..base_type import base_type
from typing import Optional

@base_type
class ChatInviteLink:
    '''
    Represents an invite link for a chat.
    '''

    is_revoked: bool
    '''
    True, if the link is revoked
    '''

    is_primary: bool
    '''
    True, if the link is primary
    '''

    creates_join_request: bool
    '''
    True, if users joining the chat via the link need to be approved by chat administrators
    '''

    creator: User
    '''
    Creator of the link
    '''

    invite_link: str
    '''
    The invite link. If the link was created by another chat administrator, then the second part of the link will be replaced with "...".
    '''

    name: Optional[str] = None
    '''
    Optional. Invite link name
    '''

    expire_date: Optional[int] = None
    '''
    Optional. Point in time (Unix timestamp) when the link will expire or has been expired
    '''

    member_limit: Optional[int] = None
    '''
    Optional. The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
    '''

    pending_join_request_count: Optional[int] = None
    '''
    Optional. Number of pending join requests created using this link
    '''

    subscription_period: Optional[int] = None
    '''
    Optional. The number of seconds the subscription will be active for before the next payment
    '''

    subscription_price: Optional[int] = None
    '''
    Optional. The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat using the link
    '''

