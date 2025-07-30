from .BaseMethod import BaseMethod

class unbanChatSenderChat(BaseMethod):
    '''
    Use this method to unban a previously banned channel chat in a supergroup or channel. The bot must be an administrator for this to work and must have the appropriate administrator rights. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param sender_chat_id: Unique identifier of the target sender chat
    :type sender_chat_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    sender_chat_id: int,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param sender_chat_id: Unique identifier of the target sender chat
        :type sender_chat_id: int
        '''
        return await self.request(
            chat_id=chat_id,
            sender_chat_id=sender_chat_id,
        )
