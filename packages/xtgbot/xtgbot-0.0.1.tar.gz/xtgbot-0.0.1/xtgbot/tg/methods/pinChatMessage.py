from .BaseMethod import BaseMethod

class pinChatMessage(BaseMethod):
    '''
    Use this method to add a message to the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages' administrator right in a channel. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be pinned
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Identifier of a message to pin
    :type message_id: int
    :param disable_notification: Pass True if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.
    :type disable_notification: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    message_id: int,
    chat_id: int |str,
    business_connection_id: str | None = None,
    disable_notification: bool = False,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be pinned
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of a message to pin
        :type message_id: int
        :param disable_notification: Pass True if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.
        :type disable_notification: bool = False
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            disable_notification=disable_notification,
        )
