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
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from .User import User
from .ChatMember import ChatMember
from ..base_type import base_type
from typing import Optional

@base_type
class ChatMemberRestricted(ChatMember):
    '''
    Represents a chat member that is under certain restrictions in the chat. Supergroups only.
    '''

    until_date: int
    '''
    Date when restrictions will be lifted for this user; Unix time. If 0, then the user is restricted forever
    '''

    can_manage_topics: bool
    '''
    True, if the user is allowed to create forum topics
    '''

    can_pin_messages: bool
    '''
    True, if the user is allowed to pin messages
    '''

    can_invite_users: bool
    '''
    True, if the user is allowed to invite new users to the chat
    '''

    can_change_info: bool
    '''
    True, if the user is allowed to change the chat title, photo and other settings
    '''

    can_add_web_page_previews: bool
    '''
    True, if the user is allowed to add web page previews to their messages
    '''

    can_send_other_messages: bool
    '''
    True, if the user is allowed to send animations, games, stickers and use inline bots
    '''

    can_send_polls: bool
    '''
    True, if the user is allowed to send polls and checklists
    '''

    can_send_voice_notes: bool
    '''
    True, if the user is allowed to send voice notes
    '''

    can_send_video_notes: bool
    '''
    True, if the user is allowed to send video notes
    '''

    can_send_videos: bool
    '''
    True, if the user is allowed to send videos
    '''

    can_send_photos: bool
    '''
    True, if the user is allowed to send photos
    '''

    can_send_documents: bool
    '''
    True, if the user is allowed to send documents
    '''

    can_send_audios: bool
    '''
    True, if the user is allowed to send audios
    '''

    can_send_messages: bool
    '''
    True, if the user is allowed to send text messages, contacts, giveaways, giveaway winners, invoices, locations and venues
    '''

    is_member: bool
    '''
    True, if the user is a member of the chat at the moment of the request
    '''

    user: User
    '''
    Information about the user
    '''

    status: str
    '''
    The member's status in the chat, always "restricted"
    '''

