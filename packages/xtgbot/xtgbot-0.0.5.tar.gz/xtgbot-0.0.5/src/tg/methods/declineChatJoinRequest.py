from .BaseMethod import BaseMethod

class declineChatJoinRequest(BaseMethod):
    '''
    Use this method to decline a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await self.request(
            chat_id=chat_id,
            user_id=user_id,
        )
