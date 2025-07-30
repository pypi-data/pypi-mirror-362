from .BaseMethod import BaseMethod

class getChatMemberCount(BaseMethod):
    '''
    Use this method to get the number of members in a chat. Returns Int on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
    :type chat_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    ) -> int:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await self.request(
            chat_id=chat_id,
        )
