from ..types.ChatMember import ChatMember
from .BaseMethod import BaseMethod

class getChatAdministrators(BaseMethod):
    '''
    Use this method to get a list of administrators in a chat, which aren't bots. Returns an Array of ChatMember objects.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
    :type chat_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    ) -> list[ChatMember]:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await self.request(
            chat_id=chat_id,
        )
