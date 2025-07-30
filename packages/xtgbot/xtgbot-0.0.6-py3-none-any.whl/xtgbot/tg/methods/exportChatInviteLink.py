from .BaseMethod import BaseMethod

class exportChatInviteLink(BaseMethod):
    '''
    Use this method to generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the new invite link as String on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    ) -> str:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await self.request(
            chat_id=chat_id,
        )
