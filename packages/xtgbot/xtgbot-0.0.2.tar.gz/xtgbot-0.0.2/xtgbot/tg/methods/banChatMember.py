from .BaseMethod import BaseMethod

class banChatMember(BaseMethod):
    '''
    Use this method to ban a user in a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the chat on their own using invite links, etc., unless unbanned first. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
    :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)
    :type chat_id: int
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :param until_date: Date when the user will be unbanned; Unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever. Applied for supergroups and channels only.
    :type until_date: int
    :param revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. If False, the user will be able to see messages in the group that were sent before the user was removed. Always True for supergroups and channels.
    :type revoke_messages: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    chat_id: int |str,
    until_date: int | None = None,
    revoke_messages: bool = False,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param until_date: Date when the user will be unbanned; Unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever. Applied for supergroups and channels only.
        :type until_date: int
        :param revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. If False, the user will be able to see messages in the group that were sent before the user was removed. Always True for supergroups and channels.
        :type revoke_messages: bool = False
        '''
        return await self.request(
            chat_id=chat_id,
            user_id=user_id,
            until_date=until_date,
            revoke_messages=revoke_messages,
        )
