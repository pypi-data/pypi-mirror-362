from ..types.ChatFullInfo import ChatFullInfo
from .BaseMethod import BaseMethod

class getChat(BaseMethod):
    '''
    Use this method to get up-to-date information about the chat. Returns a ChatFullInfo object on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
    :type chat_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    ) -> ChatFullInfo:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await self.request(
            chat_id=chat_id,
        )
