from .BaseMethod import BaseMethod

class setChatTitle(BaseMethod):
    '''
    Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param title: New chat title, 1-128 characters
    :type title: str
    :return: {tdesc}

    '''

    async def __call__(self,
    title: str,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param title: New chat title, 1-128 characters
        :type title: str
        '''
        return await self.request(
            chat_id=chat_id,
            title=title,
        )
