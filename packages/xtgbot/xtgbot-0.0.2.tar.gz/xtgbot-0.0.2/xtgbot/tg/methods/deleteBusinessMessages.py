from .BaseMethod import BaseMethod

class deleteBusinessMessages(BaseMethod):
    '''
    Delete messages on behalf of a business account. Requires the can_delete_sent_messages business bot right to delete messages sent by the bot itself, or the can_delete_all_messages business bot right to delete any message. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection on behalf of which to delete the messages
    :type business_connection_id: str
    :param message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. All messages must be from the same chat. See deleteMessage for limitations on which messages can be deleted
    :type message_ids: list[int]
    :return: {tdesc}

    '''

    async def __call__(self,
    message_ids: list[int],
    business_connection_id: str,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which to delete the messages
        :type business_connection_id: str
        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. All messages must be from the same chat. See deleteMessage for limitations on which messages can be deleted
        :type message_ids: list[int]
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            message_ids=message_ids,
        )
