from .BaseMethod import BaseMethod

class deleteChatPhoto(BaseMethod):
    '''
    Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await self.request(
            chat_id=chat_id,
        )
