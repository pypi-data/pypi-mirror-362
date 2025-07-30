from .BaseMethod import BaseMethod

class removeChatVerification(BaseMethod):
    '''
    Removes verification from a chat that is currently verified on behalf of the organization represented by the bot. Returns True on success.
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
