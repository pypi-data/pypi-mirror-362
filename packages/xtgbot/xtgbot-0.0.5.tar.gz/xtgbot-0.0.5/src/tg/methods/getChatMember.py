from ..types.ChatMember import ChatMember
from .BaseMethod import BaseMethod

class getChatMember(BaseMethod):
    '''
    Use this method to get information about a member of a chat. The method is only guaranteed to work for other users if the bot is an administrator in the chat. Returns a ChatMember object on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
    :type chat_id: int
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    chat_id: int |str,
    ) -> ChatMember:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await self.request(
            chat_id=chat_id,
            user_id=user_id,
        )
