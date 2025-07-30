from ..types.UserChatBoosts import UserChatBoosts
from .BaseMethod import BaseMethod

class getUserChatBoosts(BaseMethod):
    '''
    Use this method to get the list of boosts added to a chat by a user. Requires administrator rights in the chat. Returns a UserChatBoosts object.
    :param chat_id: Unique identifier for the chat or username of the channel (in the format @channelusername)
    :type chat_id: int
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    chat_id: int |str,
    ) -> UserChatBoosts:
        '''
        :param chat_id: Unique identifier for the chat or username of the channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await self.request(
            chat_id=chat_id,
            user_id=user_id,
        )
