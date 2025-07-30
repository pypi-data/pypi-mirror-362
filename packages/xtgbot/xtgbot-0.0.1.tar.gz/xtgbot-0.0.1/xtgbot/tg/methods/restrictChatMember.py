from ..types.ChatPermissions import ChatPermissions
from .BaseMethod import BaseMethod

class restrictChatMember(BaseMethod):
    '''
    Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate administrator rights. Pass True for all permissions to lift restrictions from a user. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    :type chat_id: int
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :param permissions: A JSON-serialized object for new user permissions
    :type permissions: ChatPermissions
    :param use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
    :type use_independent_chat_permissions: bool = False
    :param until_date: Date when restrictions will be lifted for the user; Unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever
    :type until_date: int
    :return: {tdesc}

    '''

    async def __call__(self,
    permissions: ChatPermissions,
    user_id: int,
    chat_id: int |str,
    use_independent_chat_permissions: bool = False,
    until_date: int | None = None,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param permissions: A JSON-serialized object for new user permissions
        :type permissions: ChatPermissions
        :param use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
        :type use_independent_chat_permissions: bool = False
        :param until_date: Date when restrictions will be lifted for the user; Unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever
        :type until_date: int
        '''
        return await self.request(
            chat_id=chat_id,
            user_id=user_id,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
            until_date=until_date,
        )
