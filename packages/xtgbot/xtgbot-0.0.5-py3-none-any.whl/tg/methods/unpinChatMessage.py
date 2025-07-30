from .BaseMethod import BaseMethod

class unpinChatMessage(BaseMethod):
    '''
    Use this method to remove a message from the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages' administrator right in a channel. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be unpinned
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Identifier of the message to unpin. Required if business_connection_id is specified. If not specified, the most recent pinned message (by sending date) will be unpinned.
    :type message_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    business_connection_id: str | None = None,
    message_id: int | None = None,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be unpinned
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of the message to unpin. Required if business_connection_id is specified. If not specified, the most recent pinned message (by sending date) will be unpinned.
        :type message_id: int
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
        )
