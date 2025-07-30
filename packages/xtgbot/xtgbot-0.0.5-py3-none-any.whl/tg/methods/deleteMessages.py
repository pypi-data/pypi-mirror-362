from .BaseMethod import BaseMethod

class deleteMessages(BaseMethod):
    '''
    Use this method to delete multiple messages simultaneously. If some of the specified messages can't be found, they are skipped. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. See deleteMessage for limitations on which messages can be deleted
    :type message_ids: list[int]
    :return: {tdesc}

    '''

    async def __call__(self,
    message_ids: list[int],
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. See deleteMessage for limitations on which messages can be deleted
        :type message_ids: list[int]
        '''
        return await self.request(
            chat_id=chat_id,
            message_ids=message_ids,
        )
