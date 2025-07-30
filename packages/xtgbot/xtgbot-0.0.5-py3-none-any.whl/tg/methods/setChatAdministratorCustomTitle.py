from .BaseMethod import BaseMethod

class setChatAdministratorCustomTitle(BaseMethod):
    '''
    Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    :type chat_id: int
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :param custom_title: New custom title for the administrator; 0-16 characters, emoji are not allowed
    :type custom_title: str
    :return: {tdesc}

    '''

    async def __call__(self,
    custom_title: str,
    user_id: int,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param custom_title: New custom title for the administrator; 0-16 characters, emoji are not allowed
        :type custom_title: str
        '''
        return await self.request(
            chat_id=chat_id,
            user_id=user_id,
            custom_title=custom_title,
        )
