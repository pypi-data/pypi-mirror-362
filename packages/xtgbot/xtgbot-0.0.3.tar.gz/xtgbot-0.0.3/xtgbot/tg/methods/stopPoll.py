from ..types.Poll import Poll
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from .BaseMethod import BaseMethod

class stopPoll(BaseMethod):
    '''
    Use this method to stop a poll which was sent by the bot. On success, the stopped Poll is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Identifier of the original message with the poll
    :type message_id: int
    :param reply_markup: A JSON-serialized object for a new message inline keyboard.
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    message_id: int,
    chat_id: int |str,
    business_connection_id: str | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Poll:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of the original message with the poll
        :type message_id: int
        :param reply_markup: A JSON-serialized object for a new message inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        )
