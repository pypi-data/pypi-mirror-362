from .BaseMethod import BaseMethod

class readBusinessMessage(BaseMethod):
    '''
    Marks incoming message as read on behalf of a business account. Requires the can_read_messages business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection on behalf of which to read the message
    :type business_connection_id: str
    :param chat_id: Unique identifier of the chat in which the message was received. The chat must have been active in the last 24 hours.
    :type chat_id: int
    :param message_id: Unique identifier of the message to mark as read
    :type message_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    message_id: int,
    chat_id: int,
    business_connection_id: str,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which to read the message
        :type business_connection_id: str
        :param chat_id: Unique identifier of the chat in which the message was received. The chat must have been active in the last 24 hours.
        :type chat_id: int
        :param message_id: Unique identifier of the message to mark as read
        :type message_id: int
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
        )
