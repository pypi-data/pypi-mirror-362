from .Chat import Chat
from .User import User
from .ChatMember import ChatMember
from .ChatInviteLink import ChatInviteLink
from .Chat import Chat
from .User import User
from .ChatMember import ChatMember
from .ChatInviteLink import ChatInviteLink
from .Chat import Chat
from .User import User
from .ChatMember import ChatMember
from .ChatInviteLink import ChatInviteLink
from .Chat import Chat
from .User import User
from .ChatMember import ChatMember
from .Chat import Chat
from .User import User
from .ChatMember import ChatMember
from .Chat import Chat
from .User import User
from .Chat import Chat
from .User import User
from .Chat import Chat
from ..base_type import base_type
from typing import Optional

@base_type
class ChatMemberUpdated:
    '''
    This object represents changes in the status of a chat member.
    '''

    new_chat_member: ChatMember
    '''
    New information about the chat member
    '''

    old_chat_member: ChatMember
    '''
    Previous information about the chat member
    '''

    date: int
    '''
    Date the change was done in Unix time
    '''

    from_: User
    '''
    Performer of the action, which resulted in the change
    '''

    chat: Chat
    '''
    Chat the user belongs to
    '''

    invite_link: Optional[ChatInviteLink] = None
    '''
    Optional. Chat invite link, which was used by the user to join the chat; for joining by invite link events only.
    '''

    via_join_request: bool = False
    '''
    Optional. True, if the user joined the chat after sending a direct join request without using an invite link and being approved by an administrator
    '''

    via_chat_folder_invite_link: bool = False
    '''
    Optional. True, if the user joined the chat via a chat folder invite link
    '''

