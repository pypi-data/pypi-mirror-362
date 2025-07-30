from .BaseMethod import BaseMethod

class banChatSenderChat(BaseMethod):
    '''
    Use this method to ban a channel chat in a supergroup or a channel. Until the chat is unbanned, the owner of the banned chat won't be able to send messages on behalf of any of their channels. The bot must be an administrator in the supergroup or channel for this to work and must have the appropriate administrator rights. Returns True on success.
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
