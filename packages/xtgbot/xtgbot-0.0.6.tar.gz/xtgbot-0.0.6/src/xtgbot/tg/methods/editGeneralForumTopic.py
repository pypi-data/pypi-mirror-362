from .BaseMethod import BaseMethod

class editGeneralForumTopic(BaseMethod):
    '''
    Use this method to edit the name of the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    :type chat_id: int
    :param name: New topic name, 1-128 characters
    :type name: str
    :return: {tdesc}

    '''

    async def __call__(self,
    name: str,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param name: New topic name, 1-128 characters
        :type name: str
        '''
        return await self.request(
            chat_id=chat_id,
            name=name,
        )
