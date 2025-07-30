from .BaseMethod import BaseMethod

class unpinAllGeneralForumTopicMessages(BaseMethod):
    '''
    Use this method to clear the list of pinned messages in a General forum topic. The bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    :type chat_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        '''
        return await self.request(
            chat_id=chat_id,
        )
