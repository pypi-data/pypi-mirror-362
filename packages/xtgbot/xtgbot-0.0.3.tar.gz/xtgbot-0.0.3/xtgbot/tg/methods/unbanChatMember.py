from .BaseMethod import BaseMethod

class unbanChatMember(BaseMethod):
    '''
    Use this method to unban a previously banned user in a supergroup or channel. The user will not return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. By default, this method guarantees that after the call the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat they will also be removed from the chat. If you don't want this, use the parameter only_if_banned. Returns True on success.
    :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)
    :type chat_id: int
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :param only_if_banned: Do nothing if the user is not banned
    :type only_if_banned: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    chat_id: int |str,
    only_if_banned: bool = False,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param only_if_banned: Do nothing if the user is not banned
        :type only_if_banned: bool = False
        '''
        return await self.request(
            chat_id=chat_id,
            user_id=user_id,
            only_if_banned=only_if_banned,
        )
