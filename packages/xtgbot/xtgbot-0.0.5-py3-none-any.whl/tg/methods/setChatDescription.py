from .BaseMethod import BaseMethod

class setChatDescription(BaseMethod):
    '''
    Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param description: New chat description, 0-255 characters
    :type description: str
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    description: str | None = None,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param description: New chat description, 0-255 characters
        :type description: str
        '''
        return await self.request(
            chat_id=chat_id,
            description=description,
        )
