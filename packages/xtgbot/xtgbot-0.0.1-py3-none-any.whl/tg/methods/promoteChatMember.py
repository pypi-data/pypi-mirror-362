from .BaseMethod import BaseMethod

class promoteChatMember(BaseMethod):
    '''
    Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Pass False for all boolean parameters to demote a user. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :param is_anonymous: Pass True if the administrator's presence in the chat is hidden
    :type is_anonymous: bool = False
    :param can_manage_chat: Pass True if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages, ignore slow mode, and send messages to the chat without paying Telegram Stars. Implied by any other administrator privilege.
    :type can_manage_chat: bool = False
    :param can_delete_messages: Pass True if the administrator can delete messages of other users
    :type can_delete_messages: bool = False
    :param can_manage_video_chats: Pass True if the administrator can manage video chats
    :type can_manage_video_chats: bool = False
    :param can_restrict_members: Pass True if the administrator can restrict, ban or unban chat members, or access supergroup statistics
    :type can_restrict_members: bool = False
    :param can_promote_members: Pass True if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by him)
    :type can_promote_members: bool = False
    :param can_change_info: Pass True if the administrator can change chat title, photo and other settings
    :type can_change_info: bool = False
    :param can_invite_users: Pass True if the administrator can invite new users to the chat
    :type can_invite_users: bool = False
    :param can_post_stories: Pass True if the administrator can post stories to the chat
    :type can_post_stories: bool = False
    :param can_edit_stories: Pass True if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive
    :type can_edit_stories: bool = False
    :param can_delete_stories: Pass True if the administrator can delete stories posted by other users
    :type can_delete_stories: bool = False
    :param can_post_messages: Pass True if the administrator can post messages in the channel, approve suggested posts, or access channel statistics; for channels only
    :type can_post_messages: bool = False
    :param can_edit_messages: Pass True if the administrator can edit messages of other users and can pin messages; for channels only
    :type can_edit_messages: bool = False
    :param can_pin_messages: Pass True if the administrator can pin messages; for supergroups only
    :type can_pin_messages: bool = False
    :param can_manage_topics: Pass True if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only
    :type can_manage_topics: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    chat_id: int |str,
    is_anonymous: bool = False,
    can_manage_chat: bool = False,
    can_delete_messages: bool = False,
    can_manage_video_chats: bool = False,
    can_restrict_members: bool = False,
    can_promote_members: bool = False,
    can_change_info: bool = False,
    can_invite_users: bool = False,
    can_post_stories: bool = False,
    can_edit_stories: bool = False,
    can_delete_stories: bool = False,
    can_post_messages: bool = False,
    can_edit_messages: bool = False,
    can_pin_messages: bool = False,
    can_manage_topics: bool = False,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param is_anonymous: Pass True if the administrator's presence in the chat is hidden
        :type is_anonymous: bool = False
        :param can_manage_chat: Pass True if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages, ignore slow mode, and send messages to the chat without paying Telegram Stars. Implied by any other administrator privilege.
        :type can_manage_chat: bool = False
        :param can_delete_messages: Pass True if the administrator can delete messages of other users
        :type can_delete_messages: bool = False
        :param can_manage_video_chats: Pass True if the administrator can manage video chats
        :type can_manage_video_chats: bool = False
        :param can_restrict_members: Pass True if the administrator can restrict, ban or unban chat members, or access supergroup statistics
        :type can_restrict_members: bool = False
        :param can_promote_members: Pass True if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by him)
        :type can_promote_members: bool = False
        :param can_change_info: Pass True if the administrator can change chat title, photo and other settings
        :type can_change_info: bool = False
        :param can_invite_users: Pass True if the administrator can invite new users to the chat
        :type can_invite_users: bool = False
        :param can_post_stories: Pass True if the administrator can post stories to the chat
        :type can_post_stories: bool = False
        :param can_edit_stories: Pass True if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive
        :type can_edit_stories: bool = False
        :param can_delete_stories: Pass True if the administrator can delete stories posted by other users
        :type can_delete_stories: bool = False
        :param can_post_messages: Pass True if the administrator can post messages in the channel, approve suggested posts, or access channel statistics; for channels only
        :type can_post_messages: bool = False
        :param can_edit_messages: Pass True if the administrator can edit messages of other users and can pin messages; for channels only
        :type can_edit_messages: bool = False
        :param can_pin_messages: Pass True if the administrator can pin messages; for supergroups only
        :type can_pin_messages: bool = False
        :param can_manage_topics: Pass True if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only
        :type can_manage_topics: bool = False
        '''
        return await self.request(
            chat_id=chat_id,
            user_id=user_id,
            is_anonymous=is_anonymous,
            can_manage_chat=can_manage_chat,
            can_delete_messages=can_delete_messages,
            can_manage_video_chats=can_manage_video_chats,
            can_restrict_members=can_restrict_members,
            can_promote_members=can_promote_members,
            can_change_info=can_change_info,
            can_invite_users=can_invite_users,
            can_post_stories=can_post_stories,
            can_edit_stories=can_edit_stories,
            can_delete_stories=can_delete_stories,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_pin_messages=can_pin_messages,
            can_manage_topics=can_manage_topics,
        )
