from .BaseMethod import BaseMethod

class verifyChat(BaseMethod):
    '''
    Verifies a chat on behalf of the organization which is represented by the bot. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
    :type custom_description: str
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    custom_description: str | None = None,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
        :type custom_description: str
        '''
        return await self.request(
            chat_id=chat_id,
            custom_description=custom_description,
        )
