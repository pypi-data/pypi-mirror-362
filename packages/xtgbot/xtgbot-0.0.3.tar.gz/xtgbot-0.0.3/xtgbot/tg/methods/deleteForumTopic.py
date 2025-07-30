from .BaseMethod import BaseMethod

class deleteForumTopic(BaseMethod):
    '''
    Use this method to delete a forum topic along with all its messages in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_delete_messages administrator rights. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread of the forum topic
    :type message_thread_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    message_thread_id: int,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread of the forum topic
        :type message_thread_id: int
        '''
        return await self.request(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        )
